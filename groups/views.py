from django.shortcuts import redirect, render
from django.urls import reverse,reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,DetailView,DeleteView,ListView
from .forms import GroupForm
from .models import Group,Membership
from activity.models import Activity

# Create your views here.

class BaseGroupView(LoginRequiredMixin,TemplateView):
    template_name='groups/group_base_page.html'

class GroupDetailView(LoginRequiredMixin,DetailView):
    model = Group
    template_name='groups/group_detail.html'

    def get_object(self):
        try:
            object = Group.objects.get(slug=self.kwargs['slug'])
        except Group.DoesNotExist :
            return None
        else:
            return object

class DeletegroupView(LoginRequiredMixin,DeleteView):
    model = Group
    success_url = reverse_lazy('groups:group-base')

    def delete(self, request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs['slug'])
        activity = Activity.objects.filter(user__id=request.user.id,object_id=group.id)
        activity.delete()
        return super().delete(request, *args, **kwargs)

@login_required
def CreateGroupView(request):
    if request.method == 'POST' and request.is_ajax():
        groupform = GroupForm(data=request.POST,files=request.FILES)
        if groupform.is_valid():
            group = groupform.save(commit=False)
            group.owner = request.user
            group.save()

            activity = Activity(user=request.user,content_object=group,action='created')
            activity.save()

            return render(request,'groups/group_item.html',context={'group':group})
        else:
            return JsonResponse({'status':False,'errors':str(groupform.non_field_errors())+str(groupform.errors['name'])})
    else:
        return render(request,'groups/create_group.html')

@login_required
def UpdateGroupView(request,slug):
    if request.method == 'POST' and request.is_ajax():
        group = Group.objects.get(slug=slug)
        groupform = GroupForm(data=request.POST,instance=group,files=request.FILES)
        if groupform.is_valid():
            group = groupform.save()
            activity = Activity(user=request.user,content_object=group,action='updated')
            activity.save()
            return JsonResponse({'status':True,'group':group.serialize()})
        else:
            return JsonResponse({'status':False,'errors':str(groupform.errors)+str(groupform.non_field_errors())+str(groupform.errors['name'])})
    else:
        return render(request,'groups/group-base.html')

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
           activity = Activity(user=request.user,content_object=member,action='join')
           activity.save()
           
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

           activity = Activity.objects.get(user__id=request.user.id,object_id=member.id)
           activity.delete()

           member.delete()
           
           return JsonResponse({'status':True})

       except Membership.DoesNotExist:

            return JsonResponse({'status':False})
    else:
        return redirect(reverse_lazy('groups:group-base'))


class GroupMemberListView(LoginRequiredMixin,ListView):
    model = Group
    context_object_name = 'members'
    template_name = "groups/members_list.html"

    def get_queryset(self):
        group = Group.objects.get(slug=self.kwargs['slug'])
        members = group.members.all()

        return members