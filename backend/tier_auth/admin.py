from django.contrib import admin
from .models import User, UserApiUse

admin.site.register(User)
admin.site.register(UserApiUse)