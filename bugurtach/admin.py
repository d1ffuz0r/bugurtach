from django.contrib import admin
from bugurtach.models import *

class CustomUserAdmin(admin.ModelAdmin):
    pass

class BugurtAdmin(admin.ModelAdmin):
    pass

class LikeAdmin(admin.ModelAdmin):
    list_display  = ('bugurt_id', 'user_id', 'type')

class TagAdmin(admin.ModelAdmin):
    pass

class BugurtTagsAdmin(admin.ModelAdmin):
    pass

class CommentsAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bugurt, BugurtAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BugurtTags, BugurtTagsAdmin)
admin.site.register(Comments, CommentsAdmin)
