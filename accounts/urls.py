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

]

