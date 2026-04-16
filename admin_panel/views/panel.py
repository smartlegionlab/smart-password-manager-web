from django.shortcuts import render

from admin_panel.decorators.superuser import superuser_required
from users.models import User


@superuser_required
def admin_panel_view(request):
    user_count = User.objects.count()
    context = {
        'user_count': user_count,
    }
    return render(request, 'admin_panel/admin_panel.html', context)
