from django.contrib import admin
from bugurtach.models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', )

class BugurtAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'likes', 'date')

class LikeAdmin(admin.ModelAdmin):
    list_display  = ('bugurt_id', 'user_id', 'type')

class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)

class BugurtTagsAdmin(admin.ModelAdmin):
    list_display = ('bugurt', 'tag')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'bugurt', 'date')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bugurt, BugurtAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(BugurtTags, BugurtTagsAdmin)
admin.site.register(Comments, CommentsAdmin)
