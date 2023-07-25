from apps.ocr_placa.models import OCR
from rest_framework import serializers


class OCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCR
        fields = [
            'data',
            'response',
            'status'
        ]
