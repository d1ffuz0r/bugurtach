from django.contrib import admin
from django.contrib.auth.models import Group
from bugurtach.models import Bugurt, CustomUser, Like, Tag, Proof, BugurtTags, BugurtProofs, Comments

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("user", )

class BugurtAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "likes", "date")

class LikeAdmin(admin.ModelAdmin):
    list_display  = ("bugurt_id", "user_id", "type")

class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)

class ProofAdmin(admin.ModelAdmin):
    list_display = ("link",)

class BugurtTagsAdmin(admin.ModelAdmin):
    list_display = ("bugurt", "tag")

class BugurtProofsAdmin(admin.ModelAdmin):
    list_display = ("bugurt", "proof")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("author", "bugurt", "date")

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Bugurt, BugurtAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Proof, ProofAdmin)
admin.site.register(BugurtTags, BugurtTagsAdmin)
admin.site.register(BugurtProofs, BugurtProofsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.unregister(Group)
