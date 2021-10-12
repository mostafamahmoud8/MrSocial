from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('',views.BaseGroupView.as_view(),name='group-base'),
    path('<slug:slug>/detail/',views.GroupDetailView.as_view(),name='group-detail'),
    path('create/',views.CreateGroupView,name='create-group'),
    path('delete/<slug:slug>/',views.DeletegroupView.as_view(),name='delete-group'),
    path('update/<slug:slug>/',views.UpdateGroupView,name='update-group'),
    path('search/',views.SearchGroupsView,name='search'),
    path('join/',views.JoinGroupView,name='join'),
    path('leave/',views.LeaveGroupView,name='leave'),
    path('members/<slug:slug>',views.GroupMemberListView.as_view(),name='members'),

]