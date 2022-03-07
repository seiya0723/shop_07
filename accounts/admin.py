from django.contrib import admin
from .models import CustomUserAddress, CustomUser

admin.site.register(CustomUser)
admin.site.register(CustomUserAddress)

