from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin , BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self , username , email , password =None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(username = username ,email= self.normalize_email(email))
        user.set_password(password)
        user.is_active = False
        user.save(using = self._db)
        return user

class User(AbstractBaseUser , PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100 , unique=True )
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField()
    is_verified = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True , blank=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    