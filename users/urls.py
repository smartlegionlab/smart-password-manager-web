from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users.views.auth.login import login_view
from users.views.auth.logout import logout_view
from users.views.auth.password_change import password_change_view
from users.views.auth.password_reset import password_reset_view
from users.views.auth.register import register_view
from users.views.auth.two_factor_views import (
    two_factor_backup_codes, 
    two_factor_disable, 
    two_factor_manage, 
    two_factor_setup, 
    two_factor_verify
    )
from users.views.user.user_delete import user_delete_view
from users.views.user.user_detail import user_detail_view
from users.views.user.user_update import user_update_view
from users.views.auth.password_forgot import password_forgot_view, resend_password_reset_view
from users.views.auth.verify_view import resend_verification_view, verify_email_view

app_name = 'users'

urlpatterns = [
    path('', user_detail_view, name='user_detail'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete/', user_delete_view, name='user_delete'),
    path('update/', user_update_view, name='user_update'),
    path('register/', register_view, name='register'),
    path('verify/<str:token>/', verify_email_view, name='verify_email'),
    path('resend-verification/', resend_verification_view, name='resend_verification'),
    path('password/forgot/', password_forgot_view, name='password_forgot'),
    path('password/reset/resend/', resend_password_reset_view, name='resend_password_reset'),
    path('password/reset/<token>/', password_reset_view, name='password_reset'),
    path('password/change/', password_change_view, name='password_change'),

    path('2fa/setup/', two_factor_setup, name='two_factor_setup'),
    path('2fa/backup-codes/', two_factor_backup_codes, name='two_factor_backup_codes'),
    path('2fa/manage/', two_factor_manage, name='two_factor_manage'),
    path('2fa/disable/', two_factor_disable, name='two_factor_disable'),
    path('2fa/verify/', two_factor_verify, name='two_factor_verify'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
