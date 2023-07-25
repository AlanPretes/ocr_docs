##### Imports Django
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions

##### Imports Apps
from apps.core import gateway
from .models import User
from .serializers import UserSerializer
from apps.user.utils import Utils

#Rota para obter token do usuário através de um POST, sem precisar de CSRF.
@csrf_exempt
def token(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)

        user = User.objects.get(email=email)
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'token': user.auth_token.key})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

# Aqui você pode verificar se o token é válido ou não
# Se o token for válido, você pode chamar a função de exibição
# Caso contrário, você pode retornar uma resposta de erro
class TokenRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return Response({'error': 'Token não fornecido.'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().dispatch(request, *args, **kwargs)
    
#Rota para teste
class APITESTE(TokenRequiredMixin, APIView):
    def get(self, request):
        user = User.objects.all()
        data = {'Sqad': str(user)}
        return JsonResponse(data)

class List (TokenRequiredMixin, gateway.List,):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        values = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
        page = self.paginate_queryset(values)
        serializer = UserSerializer(page, many=True)
        return gateway.response_log_user(request, self.get_paginated_response(serializer.data).data, 200)


class ListStaff(TokenRequiredMixin, gateway.List):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.filter(is_active=True, is_staff=True).order_by('first_name', 'last_name')
    serializer_class = UserSerializer


class Create(TokenRequiredMixin, gateway.Create):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            if all((request.data.get("is_staff"), request.user.is_staff)):
                serializer.save()
                Utils().set_username(serializer.data['id'], request.data['email'])

                return gateway.response_log_user(request, serializer.data, 201)

        return gateway.response_log_user(request, serializer.errors, 400)


class Retrieve(TokenRequiredMixin, gateway.Retrieve):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'id'


class Update(TokenRequiredMixin, gateway.Update):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            if 'email' in list(request.data.keys()):
                Utils().set_username(instance.id, request.data['email'])

            return gateway.response_log_user(request, serializer.data, 200)

        return gateway.response_log_user(request, serializer.errors, 400)


class Destroy(TokenRequiredMixin, gateway.Destroy):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'id'

