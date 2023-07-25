from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.user.models import User


class UserURLsTest(TestCase):
    def test_url_user_list_user(self):
        url = reverse('list_user')
        self.assertEqual(url, "/user/list")

    def test_url_user_list_user(self):
        url = reverse('list_id_user', kwargs={'id': 1})
        self.assertEqual(url, "/user/list/1/")

    def test_url_user_create_user(self):
        url = reverse('create_user')
        self.assertEqual(url, "/user/create/")

    def test_url_user_retrieve_id(self):
        url = reverse('retrieve_user', kwargs={'id': 1})
        self.assertEqual(url, "/user/retrieve/1/")

    def test_url_user_update_user(self):
        url = reverse('update_user', kwargs={'id': 1})
        self.assertEqual(url, "/user/update/1/")

    def test_url_user_destroy_user(self):
        url = reverse('destroy_user', kwargs={'id': 1})
        self.assertEqual(url, "/user/destroy/1/")


class TestViewUser(TestCase):
    def setUp(self):
        self.superuser = User.objects.create(
            email="teste@teste.com.br",
            password="teste",
            is_admin=True,
            is_superuser=True,
            is_staff=True
        )
        self.superuser.save()

    def test_view_list_user_authenticate(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        response = client.get(reverse('list_user'))
        self.assertEqual(response.status_code, 200)

    def test_view_user_list_id_authenticate(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        response = client.get(reverse('list_user'), kwargs={'id': self.superuser.id})
        self.assertEqual(response.status_code, 200)

    def test_view_user_create_user_authenticate(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        data = {
            "first_name": "Teste",
            "last_name": "Teste",
            "email": "teste@teste.com.br",
            "birth": "2022-01-01",
            "is_staff": 'True',
            "is_admin": 'True',
            "last_login": '',
            "is_active": 'True'
        }
        response = client.post(reverse('create_user'), data)
        self.assertEqual(response.status_code, 201)

    def test_view_user_retrieve_id_authenticate(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        response = client.get(f'/user/retrieve/{self.superuser.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_user_update_user_authenticate(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        data = {
            "first_name": "Teste XX",
            "last_name": "Teste",
            "email": "teste@teste.com.br",
            "birth": "2022-01-01",
            "is_staff": 'True',
            "is_admin": 'True',
            "last_login": '',
            "is_active": 'True'
        }
        response = client.put(f'/user/update/{self.superuser.id}/', data)
        self.assertEqual(response.status_code, 200)

    def test_view_user_retrieve_id_authenticate(self):
        client = APIClient()
        client.force_authenticate(self.superuser)
        response = client.delete(f'/user/destroy/{self.superuser.id}/')
        self.assertEqual(response.status_code, 204)
