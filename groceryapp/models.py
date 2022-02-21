
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError


###############################################################################################################################################


#################          Validations          ################# 

def validate_capitalized(value):
        if value != value.capitalize():
            raise ValidationError('Invalid (not capitalized) value: %(value)s',params={'value': value})
        
def only_char(value): 
    if value.isalpha()==False:
        raise ValidationError('int value not access')
    
def validate_age(value):
        if 0< value <= 100:
            return value
        raise ValidationError('Age not valid')   


###############################################################################################################################################

# User Manager
class UserManager(BaseUserManager):
    def _create_user(self, email, password,is_staff,is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        user = self._create_user(email, password, False, False, **extra_fields)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

 
 
class User(AbstractBaseUser,PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    username = models.CharField(db_index=True, max_length=255, unique=True)
    firstname=models.CharField(max_length=100,validators=[only_char],null=True)
    lastname=models.CharField(max_length=100,validators=[only_char],null=True,)
    email = models.EmailField(unique=True)
    age=models.IntegerField(null=True,validators=[validate_age]) 
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    address = models.TextField(null=True)
    
    is_enduser = models.BooleanField('Is enduser', default=False)
    is_grocery = models.BooleanField('Is grocery', default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    
    
    def __str__(self):
        return self.email
    
    
