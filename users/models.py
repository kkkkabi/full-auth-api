from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError("Users must have an email address")
        
        # normalize email means if abc@GMAil.coM  -> abc@gmail.com, only change after @
        email = self.normalize_email(email)
        email = email.lower()         # JOHN@gmail.com -> john@gmail.com


        # create user model   **kwargs means keyword variable arguments, 当函数中以列表或者元组的形式传参时，就要使用*args； 当传入字典形式的参数时，就要使用**kwargs。
        user = self.model(
            email = email,
            **kwargs
        )

        user.set_password(password) #hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

#User Account
class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)

    #we already set in Djoser, though it default True now, it will be false when create users
    #we don't change to False because when we create superuser, i won't be able to log in.
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name'] #when registering, requried fileds

    def __str__(self):
        return self.email
