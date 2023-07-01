from django.urls import path
from convert import views
urlpatterns = [
    path('api/convert/', views.ConvertImageView.as_view(), name='convert_image'),
    path('api/compress/', views.CompressImageView.as_view(), name='compress_image'),
]
