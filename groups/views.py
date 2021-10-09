from django.shortcuts import redirect, render
from django.urls import reverse,reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import GroupForm
from .models import Group,Membership

# Create your views here.

class BaseGroupView(LoginRequiredMixin,TemplateView):
    template_name='groups/group_base_page.html'


@login_required
def CreateGroupView(request):
    if request.method == 'POST' and request.is_ajax():
        groupform = GroupForm(data=request.POST,files=request.FILES)
        if groupform.is_valid():
            group = groupform.save(commit=False)
            group.owner = request.user
            group.save()

            return render(request,'groups/group_item.html',context={'group':group})
        else:
            return JsonResponse({'status':False,'errors':str(groupform.non_field_errors())+str(groupform.errors['name'])})
    else:
        return render(request,'groups/create_group.html')

@login_required
def SearchGroupsView(request):
    if  request.method == 'GET' and request.is_ajax():

        text = request.GET['search']
        groups = Group.objects.filter(name__icontains=str(text))

        return render(request,'groups/group_list.html',context={'groups':groups,'text':text})
    else:
        return redirect(reverse_lazy('groups:group-base'))

@login_required
def JoinGroupView(request):
    if  request.method == 'POST' and request.is_ajax():
       try:
           id = request.POST['groupid']
           group = Group.objects.get(id=id)
           member = Membership(group=group,user=request.user)
           member.save()
           
           return JsonResponse({'status':True})

       except Exception:
            return JsonResponse({'status':False})
    else:
        return redirect(reverse_lazy('groups:group-base'))


@login_required
def LeaveGroupView(request):
    if  request.method == 'POST' and request.is_ajax():
       try:
           id = request.POST['groupid']
           group = Group.objects.get(id=id)
           member = Membership.objects.get(group=group,user=request.user)
           member.delete()
           
           return JsonResponse({'status':True})

       except Membership.DoesNotExist:

            return JsonResponse({'status':False})
    else:
        return redirect(reverse_lazy('groups:group-base'))