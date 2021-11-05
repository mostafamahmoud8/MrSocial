from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('all/',views.AllNotificationView,name='all'),
    path('unread/',views.UnreadNotificationView,name='unread'),
    path('new/',views.NewNotificationStatusView,name='new'),
    path('change/',views.ChangeAllNotificationStatusView,name='change-all'),
    path('remove/',views.RemoveAllNotificationView,name='remove-all'),
    path('change/<int:notid>/',views.ChangeNotificationStatusView,name='change_status'),
    path('remove/<int:notid>/',views.RemoveNotificationView,name='remove'),
    path('number/',views.getNotificationNumber,name='number'),
    path('SourceEvent/',views.SourceEventNotification,name='source_event'),
]