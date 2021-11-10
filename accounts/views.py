from django.shortcuts import render ,redirect
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse
from django.http import JsonResponse
from posts.models import Share
from .forms import CustomUserCreationForm ,CustomUserChangeForm
from django.contrib.auth import get_user_model

from django.db.models import Q
from .models import FriendShip,Block

# Create your views here.

User = get_user_model()

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

class ProfileView(LoginRequiredMixin,DetailView):
    login_url = 'accounts:login'
    redirect_field_name = 'home'
    model = User
    template_name = "accounts/profile.html"
    context_object_name = 'profile'


    def get_object(self):
        try:
            object = User.objects.get(slug__iexact = self.kwargs['slug'])
        except User.DoesNotExist :
            return None
        else:
            return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userposts = []
        profile = User.objects.get(slug=self.kwargs['slug'])
        posts = profile.userposts.filter(belong_to=None).order_by('-created_at')
        sharedposts = Share.objects.select_related('post').filter(user__id=profile.id).order_by('-created_at')

        for post in posts:
            userposts.append({'post':post,'share':False,'posttype':"original",'created_at':post.created_at})
        for share in sharedposts:
            userposts.append({'post':share.post,'share':True,'shareduser':share.user,'posttype':"share",'created_at':share.created_at})
        
        userposts.sort(key=lambda posts: posts['created_at'])
        context['posts'] = userposts[::-1]

        return context

class ChangeProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'accounts/editprofile.html'

    def get_success_url(self):
        return reverse_lazy('accounts:profile',kwargs={'slug':self.request.user.slug})

class DeleteProfileView(LoginRequiredMixin,DeleteView):
    model = User
    success_url = reverse_lazy('home')

@login_required(login_url='accounts:login')  
def LogoutToResetPassword(request):
    logout(request)
    return redirect('accounts:password_reset')

## Networks view

@login_required
def NetworkBaseView(request):
     friends = []
     friendships = FriendShip.objects.filter((Q(source__id=request.user.id)
      | Q(target__id=request.user.id)) & Q(accepted=True)).select_related('source','target')
     
     for friend in friendships:
        if request.user.id == friend.source.id:
            friends.append({'user':friend.target,'date':friend.created_at})
        else:
            friends.append({'user':friend.source,'date':friend.created_at})

     sentrequests = FriendShip.objects.filter(Q(source__id=request.user.id) & Q(accepted=False))
     recieverequests = FriendShip.objects.filter(Q(target__id=request.user.id) & Q(accepted=False))
     blocks = Block.objects.filter(source__id=request.user.id)
     context = {'friends':friends,'sentrequests':sentrequests,'recieverequests':recieverequests,'blocks':blocks}

     return render(request,'networks/network_base.html',context=context)


@login_required
def SendFriendRequestView(request):
    if request.method =='POST' and request.is_ajax():
        target  = User.objects.get(id=int(request.POST['friend']))
        try:
            friend = FriendShip(source=request.user,target=target)
            friend.save()
            return JsonResponse({'status':True})
        except Exception:
            return JsonResponse({'status':False})
    else:
        return redirect('home')


@login_required
def RemoveFriendView(request):
    if request.method =='POST' and request.is_ajax():
        try:
            target  = User.objects.get(id=int(request.POST['friend']))
            friend = FriendShip.objects.get(Q(source=request.user,target=target,accepted=True) 
            | Q(source=target,target=request.user,accepted=True))
            friend.delete()

            return JsonResponse({'status':True})
        except FriendShip.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')


@login_required
def AcceptFriendRequestView(request):
    if request.method =='POST' and request.is_ajax():
        try:
            target  = User.objects.get(id=int(request.POST['friend']))
            friendship  = FriendShip.objects.get(source=target,target=request.user,accepted=False)
            friendship.accepted = True
            friendship.save()
            friend = {'user':friendship.source,'date':friendship.created_at}

            return render(request,'networks/user_item.html',context={'friend':friend})
        except Exception:
            return JsonResponse({'status':False})
    else:
        return redirect('home')

@login_required
def RefuseFriendRequestView(request):
    if request.method =='POST' and request.is_ajax():
        try:
            target  = User.objects.get(id=int(request.POST['friend']))
            friendship = FriendShip.objects.get(source=target,target=request.user,accepted=False)
            friendship.delete()
            return JsonResponse({'status':True})
        except FriendShip.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')

@login_required
def CancelFriendRequestView(request):
    if request.method =='POST' and request.is_ajax():
        try:
            target  = User.objects.get(id=int(request.POST['friend']))
            friendship = FriendShip.objects.get(source=request.user,target=target,accepted=False)
            friendship.delete()
            return JsonResponse({'status':True})
        except FriendShip.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')


@login_required
def BlockFriendView(request):
    if request.method =='POST':
        target  = User.objects.get(id=int(request.POST['friend']))
        try:
            block = Block(source=request.user,target=target)
            block.save()
            return redirect(reverse_lazy('accounts:network_base'))
        except Exception:
            return JsonResponse({'status':False})
    else:
        return redirect('home')


@login_required
def UnBlockFriendView(request):
    if request.method =='POST' and request.is_ajax():
        try:
            target  = User.objects.get(id=int(request.POST['friend']))
            block = Block.objects.get(source=request.user,target=target)
            block.delete()
            return JsonResponse({'status':True})
        except Block.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')

@login_required
def SearchFriendsView(request):
     text = str(request.GET['search'])
     myfriends = request.user.get_friends()
     users = User.objects.filter(Q(username__icontains=text)
                                 |Q(first_name__icontains=text)
                                 |Q(last_name__icontains=text))
     results = []
     for user in users:
         if user in myfriends:
             results.append(user)

     return render(request,'networks/user_search_item.html',context={'users':results})

     
     
