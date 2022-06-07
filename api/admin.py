from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Cafe)
admin.site.register(models.CafePhoneNumber)
admin.site.register(models.Place)
admin.site.register(models.Reserve)
admin.site.register(models.Cuisine)
admin.site.register(models.CafeCuisine)
