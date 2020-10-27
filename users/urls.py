from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views

from .views import signup, UserLogin, UserPublicProfile, activate, CustomPasswordResetView

urlpatterns = [
    path('signup/', signup, name='user_registration_url'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', views.LogoutView.as_view(), name='logout_url'),
    path('<slug:slug>', UserPublicProfile.as_view(), name="user_public_profile"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
