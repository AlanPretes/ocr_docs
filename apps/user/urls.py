from django.urls import path
from .views import *

urlpatterns = [
    path('api/token/', token),
    path('', APITESTE.as_view()),
    path('list/', ListStaff.as_view({"get": "list"}),name='list_user'),
    path('list/<id>/', List.as_view({"get": "list"},name='list_id_user')),
    path('create/', Create.as_view({"post": "create"}),name='create_user'),
    path('retrieve/<id>/', Retrieve.as_view({"get": "retrieve"}),name='retrieve_user'),
    path('update/<id>/', Update.as_view({"put": "update"}),name='update_user'),
    path('destroy/<id>/', Destroy.as_view({"delete": "destroy"}),name='destroy_user'),
]