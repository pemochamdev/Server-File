from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
  def create_user(self, email,password=None,**extra_fields):
    if not email:
      raise ValueError(_("The user must have an email"))
    
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    
    return user
  
  def create_superuser(self,email,password,**extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)
    
    if extra_fields.get('is_staff') is not True:
      raise ValueError(_("The superuser must have is_staff = True"))
    if extra_fields.get('is_superuser') is not True:
      raise ValueError(_("The superuser must have is_superuser = True"))
    
    return self.create_user(email, password,**extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
  email = models.EmailField(_('email'),unique=True)
  username = models.CharField(_('username'),unique=True, max_length=50)
  
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  
  
  objects = CustomUserManager()
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ("username",)
  
  def __str__(self):
      return self.email