from django.contrib import admin
from bugurtach.models import *

class CustomUserAdmin(admin.ModelAdmin):
    pass

class BugurtAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bugurt, BugurtAdmin)
