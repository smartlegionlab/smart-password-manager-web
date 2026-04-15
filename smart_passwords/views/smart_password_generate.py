from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from smart_passwords.models import SmartPassword


@login_required
def smart_password_generate_view(request, pk):
    smart_password = get_object_or_404(SmartPassword, id=pk, user=request.user)
    context = {
        'smart_password': smart_password,
        'active_page': 'manager',
    }
    return render(request, 'smart_passwords/smart_password_generate.html', context)
