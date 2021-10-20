from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Activity,AuthActivityLog
# Create your views here.

@login_required
def ActivityListView(request):
    activities = Activity.objects.filter(user__id=request.user.id).order_by('-created_at')
    authactivities = AuthActivityLog.objects.filter(user__id=request.user.id).order_by('-logtime')

    return render(request,'activity/activity_list.html',context={'activities':activities,'authactivities':authactivities})

