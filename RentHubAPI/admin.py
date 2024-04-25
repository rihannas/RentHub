from django.contrib import admin
from .models import CustomUser, Collection, Listing, Feature,Owner, Tenant, PropertyType, Image

# Register your models here.
admin.site.register(Collection)
admin.site.register(CustomUser)
admin.site.register(Listing)
admin.site.register(Feature)
admin.site.register(Owner)
admin.site.register(Tenant)
admin.site.register(PropertyType)
admin.site.register(Image)