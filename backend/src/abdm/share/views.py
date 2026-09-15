"""
Front desk API for Scan and Share.

Gate: can_create_patient (care/security/authorization/patient.py:87), the same gate as
the ABHA wizard. The desk reads shares for its facility and dismisses them when done.
"""

from care.facility.models import Facility
from care.security.authorization import AuthorizationController
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from abdm.models import AbdmProfileShare
from abdm.share import service


def _facility(facility_id):
    return get_object_or_404(Facility, external_id=facility_id)


def _authorize(request):
    if not AuthorizationController.call("can_create_patient", request.user):
        raise PermissionDenied


class ProfileShareList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, facility_id):
        _authorize(request)
        facility = _facility(facility_id)
        include_dismissed = request.query_params.get("include_dismissed") in ("1", "true")
        limit = min(max(int(request.query_params.get("limit", 50)), 1), 200)
        rows = service.inbox(facility, include_dismissed=include_dismissed, limit=limit)
        return Response({"results": [service.share_summary(row) for row in rows]})


class ProfileShareDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, facility_id, share_id):
        _authorize(request)
        facility = _facility(facility_id)
        share = get_object_or_404(AbdmProfileShare, external_id=share_id, facility=facility)
        data = service.share_summary(share)
        # The photo is sent only on the detail read, on request.
        if request.query_params.get("photo") in ("1", "true"):
            data["kycPhoto"] = (share.profile or {}).get("kycPhoto") or ""
        return Response(data)


class ProfileShareDismiss(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, facility_id, share_id):
        _authorize(request)
        facility = _facility(facility_id)
        share = get_object_or_404(AbdmProfileShare, external_id=share_id, facility=facility)
        return Response(service.share_summary(service.dismiss(share, request.user)))
