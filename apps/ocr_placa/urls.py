from django.urls import path
from .views import OCRCreate, OCRRetrieve

urlpatterns = [
    path('create/', OCRCreate.as_view({'post': 'create'})),
    path('retrieve/<id>/', OCRRetrieve.as_view({'get': 'retrieve'})),
]