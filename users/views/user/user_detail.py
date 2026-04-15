from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from auth_logs.models import UserAuthLog


@login_required
def user_detail_view(request):
    auth_logs = UserAuthLog.objects.filter(
        user=request.user
    ).order_by('-timestamp')[:5]
    context = {
        'active_page': 'profile',
        'auth_logs': auth_logs,
    }
    return render(request, 'users/user_detail.html', context)
