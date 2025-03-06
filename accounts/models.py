from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Custom Manager for Account Model
class MyAccountManager(BaseUserManager ):
  # Function to creating a regular user
  def create_user(self, first_name, last_name, username, email, password=None):
    if not email:
      raise ValueError('User Must have an email address')
    if not username:
      raise ValueError('User Must have a username')
    
    user = self.model(
      email= self.normalize_email(email),
      username = username,
      first_name=first_name,
      last_name= last_name,
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

  # Create a Superuser
  def create_superuser(self, first_name, last_name, username, email, password=None):
    user = self.create_user(
        email = email,
        username = username,
        first_name = first_name,
        last_name = last_name,
        password = password,
    )
    user.is_admin = True
    user.is_staff = True
    user.is_active = True
    user.is_superadmin = True
    user.save(using=self._db)
    return user



# Custom User Model
class Account(AbstractBaseUser, PermissionsMixin):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=100, unique=True)
  phone_number= models.CharField(max_length=15, null=True, blank=True)

  # Required Field 
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)

  objects = MyAccountManager()
 
  # Change Username as login field to Email
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS= ['username', 'first_name', 'last_name']

  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None):
    return self.is_admin or self.is_superadmin
  
  def has_module_perms(self, app_label):
    return True
  
  def save(self, *args, **kwargs):
    # Capitalize the first letter of the first name and last name
    self.first_name = self.first_name.capitalize()
    self.last_name = self.last_name.capitalize()
    super().save(*args, **kwargs)