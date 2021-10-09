from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('',views.BaseGroupView.as_view(),name='group-base'),
    path('create/',views.CreateGroupView,name='create-group'),
    path('search/',views.SearchGroupsView,name='search'),
    path('join/',views.JoinGroupView,name='join'),
    path('leave/',views.LeaveGroupView,name='leave'),

]