"""
The developer explorer API (ADR-018). Every route needs an authenticated Care user **and**
`ABDM_DEVELOPER_MODE=true`; otherwise HTTP 403 with the sentence that names the setting. `dev/status`
alone answers every authenticated user, so a screen can learn whether the explorer exists.

Every body a route returns has passed `dev.redact.redact()`: tokens, OTPs, passwords, keys and
photos are shown by name and length only, header values never (abdm-m2 design.md, "What the
integrator needs on screen"). Nothing here writes.
"""

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm import errors
from abdm.callbacks.signature import redact_headers
from abdm.dev import exchange as x
from abdm.dev import readiness, tables
from abdm.dev.redact import redact
from abdm.models import AbdmCallback, AbdmOutboundRequest
from abdm.settings import plugin_settings

OFF_SENTENCE = (
    "Developer mode is off. Set ABDM_DEVELOPER_MODE=true in the Care environment and restart Care to open "
    "the ABDM developer explorer."
)
LIST_LIMIT = 50
LIST_MAX = 200


class DeveloperModeEnabled(BasePermission):
    message = OFF_SENTENCE

    def has_permission(self, request, view):
        return bool(plugin_settings.DEVELOPER_MODE)


class DevView(APIView):
    permission_classes = [IsAuthenticated, DeveloperModeEnabled]


# --- status ----------------------------------------------------------------------------------------


class Status(APIView):
    """Is the explorer open? Any authenticated user may ask; no secret in the answer."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        enabled = bool(plugin_settings.DEVELOPER_MODE)
        body = {"enabled": enabled, "setting": "ABDM_DEVELOPER_MODE", "redaction": "name and length, never a value"}
        if enabled:
            body["hosts"] = {
                "gateway": plugin_settings.GATEWAY_URL,
                "abha": plugin_settings.ABHA_URL,
                "hsp": plugin_settings.HSP_URL,
                "cmId": plugin_settings.CM_ID,
                "callbackBase": plugin_settings.CALLBACK_BASE_URL,
            }
            body["callbackWindowSeconds"] = int(errors.CALLBACK_DEADLINE.total_seconds())
            body["states"] = list(x.STATES)
            body["modules"] = list(x.MODULES)
        return Response(body)


# --- exchanges -------------------------------------------------------------------------------------


def _ref(obj, kind: str) -> dict | None:
    if obj is None:
        return None
    return {"kind": kind, "id": str(obj.external_id), "label": str(getattr(obj, "name", "") or obj.external_id)[:120]}


def _callbacks_of(row: AbdmOutboundRequest) -> list[AbdmCallback]:
    """The callbacks that answer this row: by the foreign key the receiver set, and by
    `response.requestId` for a row the receiver could not match at the time."""
    by_fk = list(row.abdmcallback_set.order_by("received_at"))
    if by_fk:
        return by_fk
    return list(AbdmCallback.objects.filter(response_request_id=row.request_id).order_by("received_at"))


def _summary(row: AbdmOutboundRequest, callbacks: list[AbdmCallback], now) -> dict:
    first_callback = callbacks[0].received_at if callbacks else None
    state = x.state_of(
        operation_id=row.operation_id,
        status=row.status,
        http_status=row.http_status,
        sent_at=row.sent_at,
        callbacks_received=len(callbacks),
        now=now,
        window=errors.CALLBACK_DEADLINE,
    )
    body = row.request_json if isinstance(row.request_json, dict) else {}
    return {
        "requestId": row.request_id,
        "operationId": row.operation_id,
        "module": x.module_of(row.operation_id),
        "kind": x.kind_of(row.operation_id),
        "state": state,
        "reason": x.reason_of(status=row.status, http_status=row.http_status, error_code=row.error_code),
        "status": row.status,
        "httpStatus": row.http_status,
        "errorCode": row.error_code,
        "errorSummary": x.summarize_error(row.response_json) if row.status == AbdmOutboundRequest.Status.FAILED else "",
        "method": str(body.get("method") or ""),
        "path": x.path_of(str(body.get("url") or "")),
        "httpMs": x.http_ms(row.sent_at, row.completed_at),
        "callbackSeconds": x.callback_seconds(row.sent_at, first_callback),
        "callbacks": len(callbacks),
        "callbackStatuses": [c.processed_status for c in callbacks],
        "sentAt": row.sent_at,
        "completedAt": row.completed_at,
        "facility": _ref(row.facility, "facility"),
        "patient": _ref(row.patient, "patient"),
        "encounter": _ref(row.encounter, "encounter"),
    }


def _callback_detail(callback: AbdmCallback, sent_at=None) -> dict:
    return {
        "id": str(callback.external_id),
        "path": callback.path,
        "operationId": callback.operation_id,
        "receivedAt": callback.received_at,
        "seconds": x.callback_seconds(sent_at, callback.received_at) if sent_at else None,
        "requestIdHeader": callback.request_id_header,
        "responseRequestId": callback.response_request_id,
        "transactionId": callback.transaction_id,
        "hipIdHeader": callback.hip_id_header,
        "signature": {
            "status": callback.signature_status,
            "header": callback.signature_header,
            "error": callback.signature_error,
        },
        "headers": redact_headers(callback.headers_json),
        "body": redact(callback.parsed_json) if callback.parsed_json else {},
        "rawBodyChars": len(callback.raw_body or ""),
        "processed": {
            "status": callback.processed_status,
            "at": callback.processed_at,
            "error": callback.processing_error,
        },
        "rows": tables.rows_naming_callback(callback),
    }


def _parse_when(value: str):
    if not value:
        return None
    parsed = parse_datetime(value)
    if parsed is not None and timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed)
    return parsed


class Exchanges(DevView):
    """GET dev/exchanges?module=&operation=&state=&status=&facility=&patient=&encounter=&request_id=
    &since=&until=&limit=&before=: newest first, 1 row per outbound call with its callbacks joined."""

    def get(self, request):
        q = request.query_params
        queryset = AbdmOutboundRequest.objects.select_related("facility", "patient", "encounter")
        if q.get("module"):
            queryset = queryset.filter(operation_id__startswith=f"{q['module']}-")
        if q.get("operation"):
            queryset = queryset.filter(operation_id=q["operation"])
        if q.get("status"):
            queryset = queryset.filter(status=q["status"])
        for name in ("facility", "patient", "encounter"):
            if q.get(name):
                queryset = queryset.filter(**{f"{name}__external_id": q[name]})
        if q.get("request_id"):
            queryset = queryset.filter(request_id__icontains=q["request_id"].strip())
        since, until = _parse_when(q.get("since", "")), _parse_when(q.get("until", ""))
        if since:
            queryset = queryset.filter(sent_at__gte=since)
        if until:
            queryset = queryset.filter(sent_at__lte=until)
        if q.get("before"):
            anchor = AbdmOutboundRequest.objects.filter(request_id=q["before"]).values_list("pk", flat=True).first()
            if anchor is not None:
                queryset = queryset.filter(pk__lt=anchor)
        try:
            limit = min(max(int(q.get("limit") or LIST_LIMIT), 1), LIST_MAX)
        except ValueError:
            limit = LIST_LIMIT
        wanted_state = q.get("state", "")
        now = timezone.now()
        rows, more, last = [], False, ""
        # A state is derived, so the filter runs after the read: read pages until the limit fills.
        for row in queryset.order_by("-pk").iterator(chunk_size=200):
            summary = _summary(row, _callbacks_of(row), now)
            if wanted_state and summary["state"] != wanted_state:
                continue
            if len(rows) == limit:
                more = True
                break
            rows.append(summary)
            last = row.request_id
        return Response(
            {
                "rows": rows,
                "more": more,
                "next": last if more else "",
                "now": now,
                "callbackWindowSeconds": int(errors.CALLBACK_DEADLINE.total_seconds()),
            }
        )


class ExchangeDetail(DevView):
    """GET dev/exchanges/<request_id>: the call, its answer, every callback, and the rows it touched."""

    def get(self, request, request_id):
        row = get_object_or_404(
            AbdmOutboundRequest.objects.select_related("facility", "patient", "encounter"), request_id=request_id
        )
        callbacks = _callbacks_of(row)
        body = row.request_json if isinstance(row.request_json, dict) else {}
        summary = _summary(row, callbacks, timezone.now())
        answered_callback = None
        response_request_id = (
            ((body.get("body") or {}).get("response") or {}).get("requestId")
            if isinstance(body.get("body"), dict)
            else None
        )
        if response_request_id:
            # This row is our answer to an inbound callback: name it.
            inbound = AbdmCallback.objects.filter(request_id_header=response_request_id).order_by("received_at").first()
            answered_callback = _callback_detail(inbound) if inbound else None
        return Response(
            {
                **summary,
                "request": {
                    "url": str(body.get("url") or ""),
                    "method": str(body.get("method") or ""),
                    "headers": row.request_headers or {},
                    "body": redact(body.get("body") if body.get("body") is not None else {}),
                },
                "response": {
                    "status": row.http_status,
                    "headers": redact_headers(row.response_headers or {}),
                    "body": redact(row.response_json),
                    "ms": summary["httpMs"],
                },
                "callbackList": [_callback_detail(c, row.sent_at) for c in callbacks],
                "answers": answered_callback,
                "rows": tables.rows_naming_request(row),
                "failure": errors.classify(
                    code=row.error_code if row.http_status is not None else "",
                    http_status=row.http_status,
                    message=x.summarize_error(row.response_json),
                    exception=row.error_code if row.http_status is None else "",
                    request_id=row.request_id,
                    since=row.sent_at,
                ).as_dict()
                if row.status == AbdmOutboundRequest.Status.FAILED
                else None,
            }
        )


class Inbound(DevView):
    """GET dev/inbound?operation=&limit=&before=: callbacks the gateway started (discover, link init and
    confirm, consent notify, health-information request, Scan and Share), each with our ack joined
    through `body.response.requestId`."""

    def get(self, request):
        q = request.query_params
        queryset = AbdmCallback.objects.filter(outbound_request__isnull=True, response_request_id="")
        if q.get("operation"):
            queryset = queryset.filter(operation_id=q["operation"])
        if q.get("before"):
            anchor = AbdmCallback.objects.filter(external_id=q["before"]).values_list("pk", flat=True).first()
            if anchor is not None:
                queryset = queryset.filter(pk__lt=anchor)
        try:
            limit = min(max(int(q.get("limit") or LIST_LIMIT), 1), LIST_MAX)
        except ValueError:
            limit = LIST_LIMIT
        rows = list(queryset.order_by("-pk")[: limit + 1])
        more = len(rows) > limit
        rows = rows[:limit]
        out = []
        for callback in rows:
            ack = (
                AbdmOutboundRequest.objects.filter(request_json__body__response__requestId=callback.request_id_header)
                .order_by("pk")
                .first()
                if callback.request_id_header
                else None
            )
            out.append(
                {
                    **_callback_detail(callback),
                    "ack": (
                        {
                            "requestId": ack.request_id,
                            "operationId": ack.operation_id,
                            "status": ack.status,
                            "httpStatus": ack.http_status,
                            "seconds": x.callback_seconds(callback.received_at, ack.sent_at),
                        }
                        if ack
                        else None
                    ),
                }
            )
        return Response({"rows": out, "more": more, "next": str(rows[-1].external_id) if more and rows else ""})


class CallbackDetailDev(DevView):
    """GET dev/callbacks/<id>: 1 callback in full (redacted), for a link from a table row."""

    def get(self, request, callback_id):
        callback = get_object_or_404(AbdmCallback, external_id=callback_id)
        detail = _callback_detail(callback, callback.outbound_request.sent_at if callback.outbound_request else None)
        detail["answersRequestId"] = callback.outbound_request.request_id if callback.outbound_request else ""
        return Response(detail)


# --- tables ----------------------------------------------------------------------------------------


class Tables(DevView):
    def get(self, request):
        return Response({"tables": tables.table_counts()})


class TableRows(DevView):
    def get(self, request, name):
        try:
            spec = tables.spec_for(name)
        except KeyError:
            return Response({"errors": f"No table named {name}."}, status=404)
        q = request.query_params
        try:
            limit = int(q.get("limit") or tables.PAGE_LIMIT)
        except ValueError:
            limit = tables.PAGE_LIMIT
        return Response(tables.list_rows(spec, filters=dict(q.items()), before=q.get("before", ""), limit=limit))


class TableRow(DevView):
    def get(self, request, name, row_id):
        try:
            spec = tables.spec_for(name)
        except KeyError:
            return Response({"errors": f"No table named {name}."}, status=404)
        obj = tables.get_row(spec, row_id)
        if obj is None:
            return Response({"errors": "No such row."}, status=404)
        return Response(
            {
                "table": spec["name"],
                "title": spec["title"],
                "row": tables.serialize_row(obj, spec, full=True),
                "exchanges": tables.related_exchanges(obj, spec),
                "callbacks": tables.related_callbacks(obj, spec),
            }
        )


# --- readiness -------------------------------------------------------------------------------------


class Readiness(DevView):
    def get(self, request):
        return Response(readiness.readiness())
