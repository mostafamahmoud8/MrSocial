from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/',views.CreatePostView,name='create_post'),
    path('update/<int:postid>/',views.UpdatePostView,name='update_post'),
    path('delete/<int:postid>/',views.DeletePostView,name='delete_post'),
    path('add/comment/',views.CreateCommentView,name='add-comment'),
    path('update/comment/<int:commentid>/',views.UpdateCommentView,name='update-comment'),
    path('delete/comment/<int:commentid>/',views.DeleteCommentView,name='delete-comment'),
    path('add/like/<int:postid>/',views.AddLikeView,name='add-like'),
    path('remove/like/<int:postid>/',views.RemoveLikeView,name='remove-like'),
    path('share/<int:postid>/',views.ShareView,name='share'),
    path('share/remove/<int:postid>/',views.RemoveShareView,name='remove-share'),


]