from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Activity
# Create your views here.


class ActivityListView(LoginRequiredMixin,ListView):
    model = Activity
    template_name = 'activity/activity_list.html'
    context_object_name = 'activities'

    def get_queryset(self):
        activities = Activity.objects.filter(user__id=self.request.user.id)
        return activities