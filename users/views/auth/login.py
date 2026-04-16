from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.safestring import mark_safe

from users.forms.login_form import LoginForm
from users.models import User
from auth_logs.models import UserAuthLog
from core.utils.informers.request_info import RequestInfo

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache


@sensitive_post_parameters('password')
@csrf_protect
@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:user_detail')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user is None:
                messages.error(request, 'Invalid email or password!')
                return render(request, 'users/auth/login_form.html', {'form': form})

            try:
                user = User.objects.get(id=user.id)
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')
                return render(request, 'users/auth/login_form.html', {'form': form})

            if not user.is_active:
                messages.error(request, 'Account is not active! To activate, please contact your administrator.')
                return redirect('users:login')

            if not user.is_email_verified:
                resend_url = reverse('users:resend_verification')
                message = mark_safe(
                    f'Please verify your email address first. '
                    f'Check your inbox at {user.email} or '
                    f'<a href="{resend_url}?email={user.email}" class="alert-link">'
                    f'click here to resend verification email</a>'
                )
                messages.error(request, message)
                return redirect('users:login')
            
            if user.is_2fa_enabled:
                request.session['2fa_user_id'] = user.id
                messages.info(request, 'Please complete two-factor authentication.')
                return redirect('users:two_factor_verify')

            login(request, user)
            request_informer = RequestInfo(request)
            UserAuthLog.objects.create(
                user=user,
                ip=request_informer.ip,
                user_agent=request_informer.user_agent,
            )
            messages.success(request, f'{user.full_name}, welcome!')
            return redirect('users:user_detail')

        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'users/auth/login_form.html', {'form': form})
