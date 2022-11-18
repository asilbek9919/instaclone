from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from post.models import Post,Tag,Follow,Stream,Likes
from django.contrib.auth.models import User
from authly.models import Profile
from django.urls import reverse, resolve
from comment.forms import NewCommentForm
from comment.models import Comment
from django.core.paginator import Paginator
from post.forms import NewPostform
from django.db.models import Q

@login_required
def index(request):
    user = request.user
    all_user = User.objects.all()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    profile = Profile.objects.all()
    posts = Stream.objects.filter(user=user)
    group_user_ids = []

    for post in posts:
        group_user_ids.append(post.post_id)
    post_item = Post.objects.filter(id__in=group_user_ids).all().order_by('-posted')

    query = request.GET.get('q')

    if query:
        users = User.objects.filter(Q(username__icontaines=query))
        paginator = Paginator(users,8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)


    context = {
        'post_item':post_item,
        'follow_status': follow_status,
        'profile':profile,
        'all_users':all_user        
    }
    return render(request,'index.html',context)

@login_required
def NewPost(request):
    user = request.user
    profile = get_object_or_404(Profile,user=user)
    tags_obj = []

    if request.method == "POST":
        form = NewPostform(request.POST,request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture,caption=caption, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('profile',request.user.username)

    else:
        form = NewPostform()
    context = {
        'form':form
    }
    return render(request,'newpost.html', context)

@login_required
def PostDetail(request,post_id):
    user = request.user
    post = get_object_or_404(Post,id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details',args=[post.id]))
    else:
        form = NewCommentForm()

    context = {
        'post':post,
        'form':form,
        'comments':comments
    }

    return render(request, 'postdetail.html',context)

@login_required
def Tags(request,tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts':posts,
        'tag':tag
    }
    return render(request,'tag.html', context)

@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user,post=post).count()

    if not liked:
        Likes.objects.create(user=user,post=post)
        current_likes = current_likes +1
    else:
        Likes.objects.filter(user=user,post=post).delete()
        current_likes = current_likes - 1

    post.likes = current_likes
    post.save()

    return HttpResponseRedirect(reverse('post-details',args=[post_id]))

@login_required

def favourite(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favorite.filter(id=post_id).exists():
        profile.favorite.remove(post)
    else:
        profile.favorite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))

































