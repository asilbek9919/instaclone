from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from authly.models import Profile
from django.contrib.auth.models import User
from django.urls import resolve
from post.models import Post, Follow, Stream
from django.core.paginator import Paginator
from .forms import EditProfileForm, UserRegisterForm
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login





def UserProfile(request,username):
    Profile.objects.get_or_create(user=request.user)
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    posts = Post.objects.filter(user=user).order_by('-posted')

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favorite.all()

# Profile stats
    posts_count = Post.objects.filter(user=user).count()
    follower_count = Follow.objects.filter(follower=user).count()
    following_count = Follow.objects.filter(following=user).count()
    # comment_count = Comment.objects.fillter(post=posts).count()
    follow_status = Follow.objects.filter(following=user,follower=request.user).exists()

    # Paginator
    paginator = Paginator(posts, 8)
    page_number = request.GET.get('page')
    posts_paginator = paginator.get_page(page_number)


    context = {
        'posts':posts,
        'profile':profile,
        'posts_count':posts_count,
        'follower_count':follower_count,
        'following_count':following_count,
        'posts_paginator':posts_paginator
    }
    return render(request,'profile.html', context)


def EditProfile(request):
    user = request.user.id

    profile = Profile.objects.filter(user__id=user)

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.bio = form.cleaned_data.get('bio')
            profile.url = form.cleaned_data.get('url')
            profile.favorite = form.cleaned_data.get('favorite')
            profile.save()
            return redirect('profile', profile.user.username)
    else:
        form = EditProfileForm(instance=request.user.profile)
    
    context = {
        'form':form,
    }
    return render(request,'editprofile.html', context)

def follow(request, username,option):
    user = request.user
    following = get_object_or_404(User, username=username)

    try:
        f, created=Follow.objects.get_or_create(follower=request.user,following=following)

        if int(option):
            f.delete()
            Stream.objects.filter(following=following, user=request.user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:25]
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post,user=request.user,date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile',args=[username]))

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile',args=[username]))

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Curry your account was created!')

            new_user = authenticate(username=form.cleaned_data['username'])

            login(request,new_user)
            return redirect('index')
    elif request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserRegisterForm()
    context = {
        'form':form
    }
    return render(request, 'sign-up.html')






















