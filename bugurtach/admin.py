from django.contrib import admin
from bugurtach.models import *

class CustomUserAdmin(admin.ModelAdmin):
    pass

class BugurtAdmin(admin.ModelAdmin):
    pass

class LikeAdmin(admin.ModelAdmin):
    pass

class TagAdmin(admin.ModelAdmin):
    pass

class BugurtTagsAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bugurt, BugurtAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BugurtTags, BugurtTagsAdmin)
