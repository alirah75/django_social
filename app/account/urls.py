from django.urls import path
from .views import UserLoginView, UserRegisterView, UserLogoutView, UserProfileView, UserPasswordResetView, \
    UserPasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, UserFollowView, UserUnfollowView


app_name = 'account'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>', UserProfileView.as_view(), name='profile'),
    path('reset/', UserPasswordResetView.as_view(), name='reset_password'),
    path('reset/done', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id/', UserFollowView.as_view, name='user_follow'),
    path('unfollow/<int:user_id/', UserUnfollowView.as_view, name='user_unfollow'),

]
