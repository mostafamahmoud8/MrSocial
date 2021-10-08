from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('',views.BaseGroupView.as_view(),name='groups'),
    path('create/',views.CreateGroupView,name='create-group'),

]