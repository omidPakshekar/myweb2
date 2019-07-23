
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import register, edit
from django.conf import settings
from django.conf.urls.static import static

from accounts import views as accounts_view

app_name = 'myweb'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls') ),
  	path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('', include('social_django.urls', namespace='social')),
    path('images/', include('images.urls', namespace='images')),
    path('users/', accounts_view.user_list, name='user_list'),
    # make sure the user follow befour user detail bashe chon ba hrchi ke string bydad ono ghbol mikone
    path('users/follow/', accounts_view.user_follow, name='user_follow'),
    path('users/<str:username>/', accounts_view.user_detail, name='user_detail'),
    path('password-change/',
    	auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change.html'), name='password_change'),

    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
    	template_name='registration/password_change/done.html'),
    	 name='password_change_done'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password-reset/password_reset.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
     auth_views.PasswordResetDoneView.as_view(
         template_name='registration/password-reset/done.html'
     ),
     name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password-reset/password-reset-confirm.html'),

         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password-reset/password-reset-complete.html'),
             name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
