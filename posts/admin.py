from django.contrib import admin
from .models import Post,Comment,Like,Share
# Register your models here.


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 1

class SharesInline(admin.TabularInline):
    model = Like
    extra = 1

class LikessInline(admin.TabularInline):
    model = Share
    extra = 1

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id','content','owner']
    inlines = (CommentsInline,LikessInline,SharesInline,)
    


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)