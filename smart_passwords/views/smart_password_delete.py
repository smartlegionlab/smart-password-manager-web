from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from smart_passwords.services import SmartPasswordService


@login_required
def smart_password_delete_view(request, pk):
    try:
        SmartPasswordService.delete_smart_password(pk, request.user)
        messages.success(request, 'Smart Password deleted successfully!')
    except ValidationError as e:
        messages.error(request, e.messages[0])
    except Exception as e:
        print(e)
        messages.error(request, 'Error deleting smart password')
    return redirect('smart_passwords:smart_password_list')
