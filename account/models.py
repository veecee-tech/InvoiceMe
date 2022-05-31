from django.db import models

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser

from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    
    def create_user(self,account_number, phone, email, password=None):

        if account_number is None:
            raise ValueError("users Should Have an account number")

        if email is None:
            raise ValueError("users Should Have an email")
        
        user = self.model(account_number=account_number, phone=phone, email=self.normalize_email(email))
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, account_number, email=None, phone=None, password=None):
    
        if password is None:
            raise ValueError("password should not be none")

        user = self.create_user(account_number=account_number, email=email,phone=phone, password=password)

        user.is_superadmin= True
        user.is_staff = True
        user.is_admin = True
        user.role = 1
        user.is_active = True
        
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    account_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=11)

    #receipt unique number
    number_count = models.IntegerField(default=0)
    #required
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'account_number'
    REQUIRED_FIELDS = ['phone', 'email',]

    objects = UserManager()

    def __str__(self):
        return f"{self.account_number}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    
  
    user = models.OneToOneField(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='userprofile', null=False)
    business_name = models.CharField(blank=True, null=True, max_length=255)
    business_address = models.CharField(blank=True, null=True, max_length=255)
    business_logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)
    else:
        pass


