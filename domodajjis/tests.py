from domodajjis.models import *
from django.urls import reverse  
from django.test import override_settings
from rest_framework.test import APITestCase
import users.urls

class GatheringAPITest(APITestCase):
    def setUp(self):
        user_data = {
          'email': 'adefgh@gmail.com',
          'password': 'abde1235',
          'password2': 'abde1235',
          'name': '박효상'
        }
        signup_response = self.client.post('/users/signup', user_data, format='json')
        access_token = signup_response.data['access_token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        user_data = {
            'name': '룰루랄라 강남 20대 모임'
        }
        self.client.post('/gathering', user_data, format='json')

    @override_settings(DEBUG=True)
    def test_gathering_create_api_success(self):
        url = reverse('gathering_create')
        user_data = {
          'name': '30대 독서모임'
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 201)

    @override_settings(DEBUG=True)
    def test_gathering_create_api_failure1(self):
        url = reverse('gathering_create')
        user_data = {
          'name': ''
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @override_settings(DEBUG=True)
    def test_gathering_create_api_failure2(self):
        url = reverse('gathering_create')
        user_data = {
          'name': '룰루랄라 강남 20대 모임'
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @override_settings(DEBUG=True)
    def test_gathering_create_api_failure3(self):
        url = reverse('gathering_create')
        self.client.credentials(HTTP_AUTHORIZATION='')
        user_data = {
          'name': '40대 모임'
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 400)

    @override_settings(DEBUG=True)
    def test_gathering_list_api_success(self):
        url = reverse('gathering_list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    @override_settings(DEBUG=True)
    def test_gathering_list_api_failure(self):
        url = reverse('gathering_list')
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 400)
    
    @override_settings(DEBUG=True)
    def test_gathering_retrieve_api_success(self):
        gathering_id = Gathering.objects.filter(name='룰루랄라 강남 20대 모임').first().id
        url = reverse('gathering_retrieve', kwargs={'id': gathering_id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
    
    @override_settings(DEBUG=True)
    def test_gathering_retrieve_api_failure(self):
        gathering_id = Gathering.objects.filter(name='룰루랄라 강남 20대 모임').first().id
        url = reverse('gathering_retrieve', kwargs={'id': gathering_id})
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 400)