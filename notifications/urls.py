from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('',views.NotifcationListView.as_view(),name='notification_list'),
    path('change/',views.ChangeAllNotificationStatusView,name='change-all'),
    path('remove/',views.RemoveAllNotificationView,name='remove-all'),
    path('change/<int:notid>/',views.ChangeNotificationStatusView,name='change_status'),
    path('remove/<int:notid>/',views.RemoveNotificationView,name='remove'),
    path('unread/',views.getNotificationNumber,name='number'),
    path('SourceEvent/',views.SourceEventNotification,name='source_event'),
]