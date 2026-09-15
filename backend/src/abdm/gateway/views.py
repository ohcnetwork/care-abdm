"""Instance-level probes and actions: gateway session, bridge state, bridge URL registration."""

from care.facility.models import Facility
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.facility.service import get_config
from abdm.gateway import bridge
from abdm.gateway.session import GatewaySessionError, get_access_token


def _require_superuser(user) -> None:
    # CARE treats `user.is_superuser` as the instance admin (care_fe AppRouter.tsx:175).
    if not getattr(user, "is_superuser", False):
        raise PermissionDenied("Only an instance administrator can do this.")


def gateway_status() -> dict:
    try:
        token = get_access_token()
    except GatewaySessionError as e:
        return {"ok": False, "status_code": e.status_code, "request_id": e.request_id}
    return {"ok": True, "token_prefix": token[:8]}


def hip_facilities() -> list[dict]:
    """Care facilities that carry an HFR facility ID, for the admin overview."""
    rows = []
    for facility in Facility.objects.filter(extensions__abdm__facility_id__isnull=False).order_by("name"):
        config = get_config(facility)
        if not config["hip_id"]:
            continue
        rows.append(
            {
                "id": str(facility.external_id),
                "name": facility.name,
                "facility_id": config["hip_id"],
                "facility_name": config.get("facility_name", ""),
                "hip_name": config.get("hip_name", ""),
                "counters": config.get("counters", []),
                "hrp_registered_at": config.get("hrp_registered_at"),
                "last_error": config.get("last_error", ""),
            }
        )
    return rows


class GatewayStatus(APIView):
    """Can this deployment obtain a gateway session? The token is never returned."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        status = gateway_status()
        return Response(status, status=200 if status["ok"] else 502)


class BridgeState(APIView):
    """The derived callback URL plus the live gateway view of the bridge. Any staff user may read it."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(bridge.bridge_state())


class BridgeRegisterUrl(APIView):
    """Register ABDM_CALLBACK_BASE_URL/api/abdm as the bridge URL. 1 per clientId, so superuser only."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        _require_superuser(request.user)
        try:
            result = bridge.register_callback_url()
        except bridge.BridgeError as exc:
            raise ValidationError({"errors": str(exc)}) from exc
        return Response({**bridge.bridge_state(), "registration": result})


class AdminOverview(APIView):
    """Everything the instance administrator needs on 1 page: gateway session, live bridge state
    and services, and the Care facilities set up as HIPs. Superuser only."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        _require_superuser(request.user)
        state = bridge.bridge_state()
        return Response({"gateway": gateway_status(), **state, "facilities": hip_facilities()})
