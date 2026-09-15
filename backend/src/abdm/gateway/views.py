"""Instance-level probes and actions: gateway session, bridge state, bridge URL registration."""

from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.gateway import bridge
from abdm.gateway.session import GatewaySessionError, get_access_token


class GatewayStatus(APIView):
    """Can this deployment obtain a gateway session? The token is never returned."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token = get_access_token()
        except GatewaySessionError as e:
            return Response({"ok": False, "status_code": e.status_code, "request_id": e.request_id}, status=502)
        return Response({"ok": True, "token_prefix": token[:8]})


class BridgeState(APIView):
    """The derived callback URL plus the live gateway view of the bridge. Any staff user may read it."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(bridge.bridge_state())
        except bridge.BridgeError as exc:
            raise ValidationError({"errors": str(exc)}) from exc


class BridgeRegisterUrl(APIView):
    """Register ABDM_CALLBACK_BASE_URL/api/abdm as the bridge URL. 1 per clientId, so superuser only."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # CARE treats `user.is_superuser` as the instance admin (care_fe AppRouter.tsx:175).
        if not getattr(request.user, "is_superuser", False):
            raise PermissionDenied("Only an instance administrator can register the bridge URL.")
        try:
            result = bridge.register_callback_url()
        except bridge.BridgeError as exc:
            raise ValidationError({"errors": str(exc)}) from exc
        return Response({**bridge.bridge_state(), "registration": result})
