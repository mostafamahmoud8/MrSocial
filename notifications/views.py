from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import json,time
from django.http import StreamingHttpResponse
from .models import Notification
# Create your views here.

class NotifcationListView(LoginRequiredMixin,ListView):
    model = Notification
    template_name = "notifications/notification_item.html"
    context_object_name = 'notifications'

    def get_queryset(self):
        queryset = Notification.objects.filter(user__id = self.request.user.id) 
        return queryset

@login_required
def ChangeAllNotificationStatusView(request):
    if request.method == 'GET' and request.is_ajax():
        try:
            Notification.objects.filter(user__id=request.user.id).update(status = True)
            return JsonResponse({'status':True})
        except:
            return JsonResponse({'status':False})
    else:
         return redirect('home')

@login_required
def ChangeNotificationStatusView(request,notid):
    if request.method == 'GET' and request.is_ajax():
        try:
            notification = Notification.objects.get(id=notid)
            notification.status = True
            notification.save()
            return JsonResponse({"status":True})
        except:
            return JsonResponse({"status":False})
    else:
         return redirect('home')

@login_required
def RemoveAllNotificationView(request):
    if request.method == 'GET' and request.is_ajax():
        try:
            notifications=Notification.objects.filter(user__id=request.user.id)
            notifications.delete()
            return JsonResponse({"status":True})
        except Notification.DoesNotExist :
            return JsonResponse({"status":False})
    else:
         return redirect('home')

@login_required
def RemoveNotificationView(request,notid):
    if request.method == 'GET' and request.is_ajax():
        try:
            notification = Notification.objects.get(id=notid)
            notification.delete()
            return JsonResponse({"status":True})
        except Notification.DoesNotExist :
            return JsonResponse({"status":False})
    else:
         return redirect('home')

@login_required
def getNotificationNumber(request):
    if request.method == 'GET':
        unreadnotifications = Notification.objects.filter(user__id=request.user.id,status=False)
        allnotifications = Notification.objects.filter(user__id=request.user.id)

        return JsonResponse({'number':unreadnotifications.count(),'all':allnotifications.count()})
    else:
         return redirect('home')

def SourceEventNotification(request):
    def event_stream():
        while True:
            notifications = Notification.objects.filter(user__id=request.user.id,status=False)
            data = {"number":notifications.count()}
            time.sleep(3)
            yield 'data: '+json.dumps(data)+'\n\n'
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')


