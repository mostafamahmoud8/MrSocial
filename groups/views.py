from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import GroupForm

# Create your views here.

class BaseGroupView(LoginRequiredMixin,TemplateView):
    template_name='groups/groups.html'


@login_required
def CreateGroupView(request):
    if request.method == 'POST' and request.is_ajax():
        groupform = GroupForm(data=request.POST,files=request.FILES)
        if groupform.is_valid():
            group = groupform.save(commit=False)
            group.owner = request.user
            group.save()

            return render(request,'groups/group.html',context={'group':group})
        else:
            return JsonResponse({'status':False,'errors':str(groupform.non_field_errors())+str(groupform.errors['name'])})
    else:
        return render(request,'groups/create_group.html')


