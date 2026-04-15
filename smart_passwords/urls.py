from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from smart_passwords.views.smart_password_create import smart_password_create_view
from smart_passwords.views.smart_password_update import smart_password_update_view
from smart_passwords.views.smart_password_delete import smart_password_delete_view
from smart_passwords.views.smart_password_generate import smart_password_generate_view
from smart_passwords.views.smart_password_list import smart_password_list_view

app_name = 'smart_passwords'


urlpatterns = [
    path('', smart_password_list_view, name='smart_password_list'),
    path('create/', smart_password_create_view, name='smart_password_create'),
    path('<int:pk>/update/', smart_password_update_view, name='smart_password_update'),
    path('<int:pk>/delete/', smart_password_delete_view, name='smart_password_delete'),
    path('<int:pk>/generate/', smart_password_generate_view, name='smart_password_generate'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
