from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.
# custom user manager gives you more control over what user model should or should not have.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):

        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# Custom user lets you add custom fields in addition to the built in features provided by AbstractBaseUser


class User(AbstractBaseUser):
    # ADMIN = 'admin'
    # STAFF = 'staff'
    # STATUS = [
    #     (ADMIN, _('Admin User')),
    #     (STAFF, _('Staff User')),
    # ]
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(('first name'), max_length=30)
    last_name = models.CharField(('last name'), max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    @staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def __str__(self):
        return "{}".format(self.email)
