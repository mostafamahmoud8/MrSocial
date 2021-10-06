from django.shortcuts import render ,redirect
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse

from posts.models import Share
from .forms import CustomUserCreationForm ,CustomUserChangeForm
from django.contrib.auth import get_user_model
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
            object = User.objects.get(username__iexact = self.kwargs['slug'])
        except User.DoesNotExist :
            return None
        else:
            return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userposts = []
        posts = self.request.user.userposts.all().order_by('-created_at')
        sharedposts = Share.objects.select_related('post').filter(user__id=self.request.user.id).order_by('-created_at')

        for post in posts:
            userposts.append({'post':post,'share':False,'created_at':post.created_at})
        for share in sharedposts:
            userposts.append({'post':share.post,'share':True,'created_at':share.created_at})
        
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
