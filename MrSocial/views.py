from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.models import Block
from posts.models import Share,Post
from groups.models import Group
from django.db.models import Q

User = get_user_model()

def index(request):
    if request.user.is_authenticated:
        return redirect('feeds')
    else:
        return render(request,'index.html')

@login_required
def HomeView(request):
    user = request.user
    friends = user.get_friends()
    usersposts = []
    if len(friends) > 0: 
        for friend in friends:
            posts = friend.userposts.filter(belong_to=None).order_by('-created_at')
            sharedposts = Share.objects.select_related('post').filter(user__id=friend.id).order_by('-created_at')
            for post in posts:
                usersposts.append({'post':post,'share':False,'posttype':"original",'created_at':post.created_at})
            for share in sharedposts:
                usersposts.append({'post':share.post,'share':True,'shareduser':share.user,'posttype':"share",'created_at':share.created_at})
        
    usersposts.sort(key=lambda posts: posts['created_at'])
    

    return render(request,'index.html',context={'posts':usersposts[::-1]})

@login_required
def SearchView(request):
    if request.method == 'GET' and request.is_ajax():
        text = request.GET['search']
        posts = Post.objects.filter(content__icontains=text).order_by('-created_at')
        blockusers = Block.objects.filter(Q(target=request.user)).only('target__id')
        users = User.objects.filter(Q(username__icontains=text)
                                 |Q(first_name__icontains=text)
                                 |Q(last_name__icontains=text)).exclude(Q(id__in=blockusers)|Q(id__in=request.user.block.only('id')))
        
        groups = Group.objects.filter(name__icontains=text).order_by('-created_at')
        
        return render(request,'search_result.html',context={'posts':posts,'users':users,'groups':groups})