from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<slug:slug>/profile/',views.ProfileView.as_view(),name='profile'),
    path('<slug:slug>/profile/update/',views.ChangeProfileView.as_view(),name='update-profile'),
    path('<slug:slug>/profile/delete/',views.DeleteProfileView.as_view(),name='delete-profile'),
    path('change/password/',auth_views.PasswordChangeView.as_view(
            template_name='accounts/changepassword.html',
            success_url=reverse_lazy('home')),
        name='change-password'
    ),
    path('forget/password/',views.LogoutToResetPassword,name='forgetpassword'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/passwordreset.html',
            success_url=reverse_lazy('accounts:password_reset_done')
        ),
        name='password_reset'
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/passwordresetdone.html'), name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/passwordresetconfirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/passwordresetcomplete.html'), name='password_reset_complete'),
    
    #network urls

    path('networks/',views.NetworkBaseView,name='network_base'),
    path('networks/add/',views.SendFriendRequestView,name='add_friend'),
    path('networks/remove/',views.RemoveFriendView,name='remove_friend'),
    path('networks/accept/',views.AcceptFriendRequestView,name='accept_friend'),
    path('networks/refuse/',views.RefuseFriendRequestView,name='refuse_friend'),
    path('networks/cancel/',views.CancelFriendRequestView,name='cancel_friend'),
    path('networks/block/',views.BlockFriendView,name='block_friend'),
    path('networks/unblock/',views.UnBlockFriendView,name='unblock_friend'),
    path('networks/search/',views.SearchFriendsView,name='search_friend'),
]

