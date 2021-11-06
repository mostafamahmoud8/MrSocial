from django.shortcuts import redirect, render 
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from groups.models import Group
from .forms import PostForm ,CommentForm
from activity.models import Activity
from .models import Post,Comment,Like,Share
# Create your views here.

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

@login_required(login_url='accounts:login')
def CreatePostView(request):
    if request.method =='POST' and request.is_ajax():
        postform = PostForm(data=request.POST,files=request.FILES)
        groupid = request.POST['belong_to']
        if postform.is_valid():
            post = postform.save(commit=False)
            post.owner = request.user
            if groupid != 'None':
                group = Group.objects.get(id=int(groupid))
                post.belong_to=group 
            post.save()

 
            return render(request,'posts/post.html',context={'post':post,'detail':False})
        else:
            return JsonResponse({'status':False,'errors':str(postform.non_field_errors())})
    else:
        return redirect('home')

@login_required(login_url='accounts:login')
def UpdatePostView(request,postid):
    if request.method == "POST" and request.is_ajax():

        post = Post.objects.get(id=postid)
        if 'clear' in request.POST:
            post.image = None
        postform  = PostForm(data=request.POST,instance=post,files=request.FILES)
       
        if postform.is_valid(): 

            post = postform.save()

            return JsonResponse({'status':True,'post':post.serialize()})         
        else:
            return JsonResponse({'status':False,'errors':str(postform.non_field_errors())})
    else:
        return redirect('home')

@login_required(login_url='accounts:login')
def DeletePostView(request,postid):
    if request.method == "POST" and request.is_ajax():
        try:
            post = Post.objects.get(id=postid)
            post.delete()

            return JsonResponse({'status':True}) 
        except Post.DoesNotExist:
            return redirect('home')
    else:
        return redirect('home')


@login_required(login_url='accounts:login')
def CreateCommentView(request):
    if request.method =='POST' and request.is_ajax():
        commentform = CommentForm(data=request.POST)
        post = Post.objects.get(id = request.POST.get('post'))
        if commentform.is_valid():
            comment = commentform.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
 
            return render(request,'posts/comment.html',context={'comment':comment})
        else:
            return JsonResponse({'status':False,'errors':str(commentform.non_field_errors())})
    else:
        return redirect('home')

@login_required(login_url='accounts:login')
def UpdateCommentView(request,commentid):
    if request.method =='POST' and request.is_ajax():
        comment = Comment.objects.get(id=commentid)
        commentform = CommentForm(data=request.POST,instance=comment)
        if commentform.is_valid():
            comment = commentform.save()
            
            return JsonResponse({'status':True,'message':comment.message})
        else:
            return JsonResponse({'status':False,'errors':str(commentform.non_field_errors())})
    else:
        return redirect('home')

@login_required(login_url='accounts:login')
def DeleteCommentView(request,commentid):
    if request.method =='POST' and request.is_ajax():
        try:
            comment = Comment.objects.get(id=commentid)
            comment.delete()

            return JsonResponse({'status':True})
        except Comment.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')

@login_required(login_url='accounts:login')
def AddLikeView(request,postid):
    if request.method =='POST' and request.is_ajax():
        post = Post.objects.get(id=postid)
        try:
            like = Like(post=post,user=request.user)
            like.save()
            likes = post.getLikes()

            return render(request,'posts/like_post_list.html',context={'likes':likes,'postid':postid})
        except Comment.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')

@login_required(login_url='accounts:login')
def RemoveLikeView(request,postid):
    if request.method =='POST' and request.is_ajax():
        post = Post.objects.get(id=postid)
        try:

            like = Like.objects.get(post__id=post.id,user__id=request.user.id)
            like.delete()
            likes = post.getLikes()

            return render(request,'posts/like_post_list.html',context={'likes':likes,'postid':postid})
        except Comment.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')


@login_required(login_url='accounts:login')
def ShareView(request,postid):
    if request.method =='POST' and request.is_ajax():
        post = Post.objects.get(id=postid)
        try:
            share = Share(post=post,user=request.user)
            share.save()
            shares = post.getShares()

            return render(request,'posts/share_post_list.html',context={'shares':shares,'postid':postid})
        except Comment.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')

@login_required(login_url='accounts:login')
def RemoveShareView(request,postid):
    if request.method =='POST' and request.is_ajax():
        post = Post.objects.get(id=postid)
        try:
            share = Share.objects.get(post__id=post.id,user__id=request.user.id)
            share.delete()
            shares = post.getShares()
            
            return render(request,'posts/share_post_list.html',context={'shares':shares,'postid':postid})
        except Comment.DoesNotExist:
            return JsonResponse({'status':False})
    else:
        return redirect('home')

@login_required
def GetNewPostsView(request):
    if request.method =='GET' and request.is_ajax():
        usersposts = []
        posts = Post.objects.filter(sent=False,owner__in=request.user.get_friends())
        shares = Share.objects.filter(sent=False,user__in=request.user.get_friends())
    
        for post in posts: 
            usersposts.append({'post':post,'share':False,'posttype':"original",'created_at':post.created_at})
        for share in shares:
            usersposts.append({'post':share.post,'share':True,'shareduser':share.user,'posttype':"share",'created_at':share.created_at})
        
        posts.update(sent=True)
        shares.update(sent=True)
        usersposts.sort(key=lambda posts: posts['created_at'])
        return render(request,'posts/post_list.html',context={'posts':usersposts[::-1]})
    else:
        return redirect('home')





