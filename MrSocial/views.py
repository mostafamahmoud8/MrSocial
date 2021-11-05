from django.shortcuts import redirect, render
from posts.models import Share

def index(request):
    if request.user.is_authenticated:
        return redirect('feeds')
    else:
        return render(request,'index.html')


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