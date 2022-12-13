from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
      def create_user(self, email, password, **extra_fields):
          if not email: 
             raise ValueError('EMAIL ADDRESS REQUIRED')
          email = self.normalize_email(email)
          user = self.model(email=email, **extra_fields)
          user.set_password(password)
          user.save(using=self._db)
          return user 
      def create_superuser(self, email, password, **extra_fields):
          # Create a SuperUser with the given email & password
          extra_fields.setdefault('is_staff', True)
          extra_fields.setdefault('is_superuser', True)
          extra_fields.setdefault('is_active', True)
          return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
      name = models.CharField(max_length=30)
      email = models.EmailField(max_length=100, unique=True)
      phone_number = models.CharField(max_length=100, unique=True)
      password = models.CharField(max_length=255)
      sns_type = models.CharField(max_length=50, null=True)
      birthday = models.PositiveBigIntegerField(null=True)
      profile_img_url = models.URLField(max_length=200, null=True)
      created_at = models.DateTimeField(auto_now_add=True)
      deleted_at = models.DateTimeField(null=True)
      
      # Remove the username field from the user model 
      username = None 
      first_name = None
      last_name = None
      date_joined = None
      last_login = None
      is_staff = None 
      is_active = None

      # Set the email field as the username field for the user model 
      USERNAME_FIELD = 'email' 
      
      # Remove 'email' from the 'REQUIRED_FIELDS' 
      REQUIRED_FIELDS = [] 

      # To use the custom UserManager class as the objects attribute for the user model 
      objects = UserManager()
      
      class Meta:
            db_table = 'users'

      def __str__(self):
          return self.name + ': ' + self.email
