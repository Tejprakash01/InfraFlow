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

class NCRViewSet(viewsets.ModelViewSet):
    queryset = NCR.objects.all()
    serializer_class = NCRSerializer
    permission_classes = [permissions.IsAuthenticated]

class VariationViewSet(viewsets.ModelViewSet):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer
    permission_classes = [permissions.IsAuthenticated]

class EOTViewSet(viewsets.ModelViewSet):
    queryset = EOT.objects.all()
    serializer_class = EOTSerializer
    permission_classes = [permissions.IsAuthenticated]
