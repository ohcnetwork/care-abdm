"""
The generic, read-only browser over the plug's tables (ADR-018). The declarations are in
`table_specs.py` (pure); this module binds them to the models and serializes rows.

A row goes out with every secret column redacted by name and length (`redact_fields`), every JSON
column through `redact()`, a heavy column (a decrypted bundle) as its size only, and every foreign
key as a small reference a browser can follow: a plug row names its table and external id, a Care
row (facility, patient, encounter, user) its kind and external id.
"""

from django.db import models as dj_models

from abdm import models
from abdm.dev.redact import redact, redact_fields
from abdm.dev.table_specs import TABLE_BY_NAME, TABLE_SPECS

MODEL_BY_NAME = {spec["name"]: getattr(models, spec["model"]) for spec in TABLE_SPECS}
TABLE_NAME_BY_MODEL = {getattr(models, spec["model"]): spec["name"] for spec in TABLE_SPECS}

# Care rows a plug row points at, by model label.
CARE_KINDS = {
    "facility.Facility": "facility",
    "emr.Patient": "patient",
    "emr.Encounter": "encounter",
    "users.User": "user",
}

PAGE_LIMIT = 50
PAGE_MAX = 200


def spec_for(name: str) -> dict:
    spec = TABLE_BY_NAME.get(name)
    if spec is None:
        raise KeyError(name)
    return spec


def reference(obj) -> dict | None:
    """A small pointer to a related row: `{table, id, label}` for a plug row, `{kind, id, label}` for
    a Care row. Never the row itself."""
    if obj is None:
        return None
    label = str(obj)
    if type(obj) in TABLE_NAME_BY_MODEL:
        return {"table": TABLE_NAME_BY_MODEL[type(obj)], "id": str(obj.external_id), "label": label[:120]}
    kind = CARE_KINDS.get(obj._meta.label)
    if kind is None:
        return {"kind": obj._meta.label, "id": str(getattr(obj, "external_id", obj.pk)), "label": label[:120]}
    name = getattr(obj, "name", None) or getattr(obj, "username", None) or label
    return {"kind": kind, "id": str(getattr(obj, "external_id", obj.pk)), "label": str(name)[:120]}


def _field_value(obj, field: dj_models.Field):
    if isinstance(field, (dj_models.ForeignKey, dj_models.OneToOneField)):
        return reference(getattr(obj, field.name))
    return getattr(obj, field.attname)


def serialize_row(obj, spec: dict, *, full: bool = False) -> dict:
    """The row as a dict. `full=False` gives the list columns; `full=True` every column."""
    names = spec["list_fields"] if not full else [f.name for f in obj._meta.concrete_fields if f.name != "id"]
    out = {"id": str(obj.external_id)}
    for name in names:
        field = obj._meta.get_field(name)
        if name in spec["heavy_fields"]:
            value = getattr(obj, field.attname)
            text = str(value) if value not in (None, "", {}, []) else ""
            out[name] = f"<{len(text)} chars, omitted>" if text else value
            continue
        out[name] = _field_value(obj, field)
    return redact_fields(out, spec["secret_fields"])


def list_rows(spec: dict, *, filters: dict, before: str = "", limit: int = PAGE_LIMIT) -> dict:
    model = MODEL_BY_NAME[spec["name"]]
    queryset = model.objects.all()
    for name in spec["filters"]:
        value = str(filters.get(name) or "").strip()
        if not value:
            continue
        field = model._meta.get_field(name)
        if isinstance(field, (dj_models.ForeignKey, dj_models.OneToOneField)):
            queryset = queryset.filter(**{f"{name}__external_id": value})
        else:
            queryset = queryset.filter(**{name: value})
    if before:
        anchor = model.objects.filter(external_id=before).values_list("pk", flat=True).first()
        if anchor is not None:
            queryset = queryset.filter(pk__lt=anchor)
    limit = min(max(int(limit or PAGE_LIMIT), 1), PAGE_MAX)
    rows = list(queryset.order_by("-pk")[: limit + 1])
    more = len(rows) > limit
    rows = rows[:limit]
    return {
        "table": spec["name"],
        "title": spec["title"],
        "module": spec["module"],
        "columns": ["id", *spec["list_fields"]],
        "filters": list(spec["filters"]),
        "rows": [serialize_row(obj, spec) for obj in rows],
        "more": more,
        "next": str(rows[-1].external_id) if more and rows else "",
    }


def table_counts() -> list[dict]:
    out = []
    for spec in TABLE_SPECS:
        model = MODEL_BY_NAME[spec["name"]]
        out.append(
            {
                "name": spec["name"],
                "title": spec["title"],
                "module": spec["module"],
                "model": spec["model"],
                "count": model.objects.count(),
                "columns": ["id", *spec["list_fields"]],
                "filters": list(spec["filters"]),
                "secretFields": list(spec["secret_fields"]),
            }
        )
    return out


def get_row(spec: dict, external_id: str):
    return MODEL_BY_NAME[spec["name"]].objects.filter(external_id=external_id).first()


def related_exchanges(obj, spec: dict) -> list[dict]:
    """The exchanges a row names through its request foreign keys, as references."""
    out = []
    for name in spec["request_fields"]:
        request = getattr(obj, name, None)
        if request is not None:
            out.append({"field": name, "requestId": request.request_id, "operationId": request.operation_id})
    return out


def related_callbacks(obj, spec: dict) -> list[dict]:
    out = []
    for name in spec["callback_fields"]:
        callback = getattr(obj, name, None)
        if callback is not None:
            out.append({"field": name, "id": str(callback.external_id), "path": callback.path})
    return out


def rows_naming_request(request) -> list[dict]:
    """Every plug row whose request foreign key points at this exchange (the link token the call
    produced, the care context it linked, the consent request it opened ...)."""
    out = []
    for spec in TABLE_SPECS:
        model = MODEL_BY_NAME[spec["name"]]
        for name in spec["request_fields"]:
            for obj in model.objects.filter(**{name: request})[:20]:
                out.append({"field": name, **(reference(obj) or {})})
    return out


def rows_naming_callback(callback) -> list[dict]:
    out = []
    for spec in TABLE_SPECS:
        model = MODEL_BY_NAME[spec["name"]]
        for name in spec["callback_fields"]:
            for obj in model.objects.filter(**{name: callback})[:20]:
                out.append({"field": name, **(reference(obj) or {})})
    return out


def redacted_json(value):
    return redact(value)
