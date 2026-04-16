from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def smart_password_create_view(request):
    context = {
        'active_page': 'manager',
    }
    return render(request, 'smart_passwords/smart_password_create.html', context)
