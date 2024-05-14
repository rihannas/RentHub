from django.db import models
from django.contrib.auth.models import Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
import phonenumbers

# Creating groups
Owner_group, Owner_created = Group.objects.get_or_create(name='Owner')
Tenant_group, Tenant_created = Group.objects.get_or_create(name='Tenant')

# Create your models here.

class CustomUserManager(BaseUserManager):
    '''Custom User Manger '''
    def create_user(self, username, email, password, **extra_fields):
        '''
            Returns: User object
            Creates a user
        '''
        if not email:
            raise ValueError('The Email field must be filled')
        email = self.normalize_email(email)
        user = self.model(username=username.strip(),  email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
            "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
            "Superuser must have is_superuser=True."
            )

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=False)
    last_login = models.DateTimeField(auto_now=True) #auto_now gets overwritten by a new a date when the object is accessed
    about = models.TextField(max_length=500, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'first_name', 'phone_number', 'password']

class OwnerManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        '''
        Returns: queryset
        Queries & Returns the users that belong to Owner group only 
        '''
        return super().get_queryset(*args, **kwargs).filter(groups=Owner_group)


    '''
    NOTE:
    This create_user function was supposed to add on the parent create_user function, where it creates a user and adds it in a group automatically
    when creating a user object you should you Owner.objects.create_user() and NOT Owner.objects.create()
    Based on my research until 25/4/24: The best place to add a user to a group is in the view ( so might change this :) )
    '''
    def create_user(self, username, email, password, **extra_fields):
        '''
        Returns: user object
        Creates a user and adds to the Owner group
        '''
    
        user = super().create_user(username, email, password, **extra_fields)
        user.groups.add(Owner_group)  # Adds user to the 'Owner' group
        user.save()
        return user


class Owner(CustomUser):
    class Meta:
        proxy = True

    objects = OwnerManager()

    '''
    Note: 

    I previously wrote this function ⬇️ 
    I was altering the save function so it add the created user, to its respective group.
    This will code will lead to value error as you're attempting to add a user to a many-to-many relationship field, such as a group membership, before the user has been saved to the database and assigned an id value.
    def save(self, *args, **kwargs):
    if not self.pk:
        self.groups.add(Owner_group)
        return super().save(*args, **kwargs)

    '''


# when a class inheirts custom user, the inherting class should also be inherting the custom user manager, in its user manager
class TenantManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs) -> models.QuerySet:
        '''
        Returns: queryset
        Queries & Returns the users that belong to Tenant group only 
        '''
        return super().get_queryset(*args, **kwargs).filter(groups=Tenant_group)

    '''
    NOTE:
    This create_user function was supposed to add on the parent create_user function, where it creates a user and adds it in a group automatically
    when creating a user object you should you Tenant.objects.create_user() and NOT Tenant.objects.create()
    Based on my research until 25/4/24: The best place to add a user to a group is in the view ( so might change this :) )
    '''
    def create_user(self, username, email, password, **extra_fields):
        '''
        Returns: user object
        Creates a user and adds to the Tenant group
        '''
        user = super().create_user(username, email, password, **extra_fields)
        user.groups.add(Tenant_group)  # Adds user to the 'Tenant' group

        user.save()
        return user

class Tenant(CustomUser):

    class Meta:
        proxy = True

    objects = TenantManager()

    '''
    Note: 

    I previously wrote this function ⬇️ 
    I was altering the save function so it add the created user, to its respective group.
    This will code will lead to value error as you're attempting to add a user to a many-to-many relationship field, such as a group membership, before the user has been saved to the database and assigned an id value.
    def save(self, *args, **kwargs):
    if not self.pk:
        self.groups.add(Owner_group)
        return super().save(*args, **kwargs)

    '''

class PropertyType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=250) #can be a link to google maps, or embed google maps and let ppl pin the location
    area = models.DecimalField(max_digits=10, decimal_places=3) # can be broken to country, city?
    date_listed = models.DateTimeField(auto_now_add=True)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms =models.IntegerField()
    bathroom = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    property_type = models.ManyToManyField(PropertyType)
    feature = models.ManyToManyField(Feature, blank=True)

    def __str__(self) -> str:
        return self.title

class Collection(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing)


class Image(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    images = models.ImageField()

