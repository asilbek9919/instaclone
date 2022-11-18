from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from authly.views import UserProfile,EditProfile


urlpatterns = [
    path('profile/edit',EditProfile,name='editprofile' ),
    path('sign-up/',auth_views.LoginView.as_view(template_name="sign-in.html", redirect_authenticated_user=True),name='sign-in'),
    path('sign-out/',auth_views.LogoutView.as_view(template_name="sign-out.html"),name='sign-out')
]
























