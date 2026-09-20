from rest_framework import viewsets, permissions
from .models import SiteInspection, RFI, NCR, Variation, EOT
from .serializers import SiteInspectionSerializer, RFISerializer, NCRSerializer, VariationSerializer, EOTSerializer

class SiteInspectionViewSet(viewsets.ModelViewSet):
    queryset = SiteInspection.objects.all()
    serializer_class = SiteInspectionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RFIViewSet(viewsets.ModelViewSet):
    queryset = RFI.objects.all()
    serializer_class = RFISerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        count = RFI.objects.count() + 1
        serializer.save(
            created_by=self.request.user,
            rfi_number=f"RFI-2026-{count:04d}"
        )

class NCRViewSet(viewsets.ModelViewSet):
    queryset = NCR.objects.all()
    serializer_class = NCRSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        count = NCR.objects.count() + 1
        serializer.save(
            created_by=self.request.user,
            ncr_number=f"NCR-2026-{count:04d}"
        )

class VariationViewSet(viewsets.ModelViewSet):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer
    permission_classes = [permissions.IsAuthenticated]

class EOTViewSet(viewsets.ModelViewSet):
    queryset = EOT.objects.all()
    serializer_class = EOTSerializer
    permission_classes = [permissions.IsAuthenticated]
