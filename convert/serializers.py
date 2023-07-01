from rest_framework import serializers
from convert.models import Image


class ConvertImageSerializer(serializers.Serializer):
    class Meta:
        model = Image
        fields = '__all__'
        source_image = serializers.ImageField()
        destination_format = serializers.CharField()


class CompressImageSerializer(serializers.Serializer):
    class Meta:
        model = Image
        fields = '__all__'
        source_image = serializers.ImageField()
        compression_ratio = serializers.FloatField()
