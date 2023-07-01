from PIL import Image as PILImage
import io
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from convert.serializers import ConvertImageSerializer, CompressImageSerializer

from convert.models import Image


class ConvertImageView(APIView):
    model = Image
    serializers = ConvertImageSerializer

    def post(self, request):
        source_image = request.FILES.get('source_image')
        destination_format = request.data.get('destination_format')

        if not source_image or not destination_format:
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        allowed_formats = ['png', 'jpeg']
        if source_image.name.split('.')[
            -1].lower() not in allowed_formats or destination_format.lower() not in allowed_formats:
            return Response({'error': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)


class CompressImageView(APIView):
    model = Image
    serializers = CompressImageSerializer

    def post(self, request):
        source_image = request.FILES.get('source_image')
        compression_ratio = request.data.get('compression_ratio')

        if not source_image or not compression_ratio:
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        allowed_formats = ['png', 'jpeg']
        if source_image.name.split('.')[-1].lower() not in allowed_formats:
            return Response({'error': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = PILImage.open(source_image)
        except Exception as e:
            return Response({'error': 'Failed to open source image'}, status=status.HTTP_400_BAD_REQUEST)

        compressed_image_buffer = io.BytesIO()
        try:
            image.save(compressed_image_buffer, format=image.format, quality=int(compression_ratio * 100))
        except Exception as e:
            return Response({'error': 'Failed to compress image'}, status=status.HTTP_400_BAD_REQUEST)

        new_image_name = source_image.name

        new_image = Image()
        new_image.image.save(new_image_name, compressed_image_buffer)

        return Response({'message': 'Image compressed successfully.', 'new_image': new_image.image.url},
                        status=status.HTTP_200_OK)
