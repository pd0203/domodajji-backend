from users.models import User
from django.urls import reverse  
from django.test import override_settings
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import make_password

# # TestCase 작성시 Rules
# # 1. 하나의 API에 대해 성공 케이스와 실패 케이스 모두 작성
# # 2. 성공 케이스 & 실패 케이스 각 1개씩 작성  
# # 3. test 파일의 이름은 test로 시작
# # 4. test 파일내 test 함수명은 test로 시작 

class UserSignUpTest(APITestCase):
    def setUp(self):
        User.objects.create(
            email = "adefg@gmail.com",
            password = "abde1235",
            name = "김한길"
        )

    @override_settings(DEBUG=True)
    def test_signup_success(self): 
        url = reverse("signup")
        user_data = {
          "email": "adefgh@gmail.com",
          "password": "abde1235",
          "password2": "abde1235",
          "name": "박효상"
        }
        response = self.client.post(url, user_data, format='json')
        print("response", response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
    
    @override_settings(DEBUG=True)        
    def test_signup_failure1(self): 
        url = reverse("signup")
        user_data = {
          "email": "abcd@gmail.com",
          "password": "1235",
          "password2": "1235",
          "name": "April"
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 400)

    @override_settings(DEBUG=True)        
    def test_signup_failure2(self): 
        url = reverse("signup")
        user_data = {
          "email": "abcd",
          "password": "abcd1235",
          "password2": "abcd1235",
          "name": "Aprils"
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 400)
    
    @override_settings(DEBUG=True)        
    def test_signup_failure3(self): 
        url = reverse("signup")
        user_data = {
          "email": "adefghhh@gmail.com",
          "password": "abcd1235",
          "password2": "abcd1235",
          "name": "김한길"
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 400)

class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email = "adefg@gmail.com",
            password = make_password("abde1235")
        )

    @override_settings(DEBUG=True)
    def test_login_success(self):
        url = reverse("login")
        user_data = {
          "email": "adefg@gmail.com",
          "password": "abde1235"
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 200)

    @override_settings(DEBUG=True)
    def test_login_failure(self):
        url = reverse("login")
        user_data = {
          "email": "adefgfgfgfg@gmail.com",
          "password": "abde1235"
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, 404)

# class UserInfoTest(APITestCase):
#     @override_settings(DEBUG=True)
#     def test_user_list_success(self):
#       # make a GET request to the user list endpoint
#       response = self.client.get('/users/')
  
#       # assert that the response has a 200 status code (success)
#       self.assertEqual(response.status_code, 200)
  
#       # assert that the response data includes the expected number of users
#       self.assertEqual(len(response.data), 10)
  
#       # assert that the response data includes the expected user data
#       for user in response.data:
#         self.assertIn('id', user)
#         self.assertIn('username', user)
#         self.assertIn('email', user)

# # class UserFindingEmailTest(APITestCase):
# #     @override_settings(DEBUG=True)
# #     def test_find_email_success(self):
# #         url = reverse("find_email") 
# #         user_data = {
# #             "name": "박효상", 
# #             "phone_number": "01096408104"
# #         }
# #         response = self.client.post(url, user_data, format='json')
# #         response_email = response.data['email']
# #         correct_email = "pd0217@naver.com"
# #         self.assertEqual(response.status_code, 200)
# #         self.assertEqual(response_email, correct_email)
    
# #     # 잘못된 이름 백엔드 전송시 DB 조회 실패로 에러 
# #     @override_settings(DEBUG=True)
# #     def test_find_email_failure(self):
# #         url = reverse("find_email") 
# #         user_data = {
# #             "name": "박효싱", 
# #             "phone_number": "01096408104"
# #         }
# #         response = self.client.post(url, user_data, format='json')
# #         response_email = response.data['email']
# #         correct_email = "pd0217@naver.com"
# #         self.assertEqual(response.status_code, 400)
# #         self.assertEqual(response_email, correct_email)

# # class UserFindingPasswordTest(APITestCase):
# #     @override_settings(DEBUG=True)
# #     def test_find_password_success(self):
# #         url = reverse("find_password") 
# #         user_data = {
# #             "name": "박효상", 
# #             "phone_number": "01096408104",
# #             "email": "pd0217@naver.com"
# #         }
# #         response = self.client.post(url, user_data, format='json')
# #         self.assertEqual(response.status_code, 200)
   
# #     # 잘못된 이메일 백엔드 전송시 DB 조회 실패로 에러
# #     @override_settings(DEBUG=True)
# #     def test_find_password_failure(self):
# #         url = reverse("find_password") 
# #         user_data = {
# #             "name": "박효상", 
# #             "phone_number": "01096408104",
# #             "email": "pd0216@naver.com"
# #         }
# #         response = self.client.post(url, user_data, format='json')
# #         self.assertEqual(response.status_code, 400)