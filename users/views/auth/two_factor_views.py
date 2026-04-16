from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
import pyotp
import qrcode
from io import BytesIO
import base64

from users.forms.two_factor_forms import Enable2FAForm, Disable2FAForm, TwoFactorLoginForm
from users.models import User


@never_cache
@require_http_methods(['GET', 'POST'])
def two_factor_verify(request):
    user_id = request.session.get('2fa_user_id')
    
    if not user_id:
        messages.error(request, 'Session expired. Please login again.')
        return redirect('users:login')
    
    user = get_object_or_404(User, id=user_id)
    
    session_key = f'2fa_failed_attempts_{user_id}'
    failed_attempts = request.session.get(session_key, 0)
    max_attempts = 3
    remaining_attempts = max_attempts - failed_attempts
    
    if failed_attempts >= max_attempts:
        messages.error(request, 'Too many failed attempts. Please login again.')
        request.session.pop('2fa_user_id', None)
        request.session.pop('2fa_next_url', None)
        request.session.pop(session_key, None)
        return redirect('users:login')
    
    if request.method == 'POST':
        form = TwoFactorLoginForm(user, request.POST)
        if form.is_valid():
            request.session.pop('2fa_user_id', None)
            request.session.pop('2fa_next_url', None)
            request.session.pop(session_key, None)
            
            login(request, user)
            messages.success(request, f'{user.full_name}, welcome!')
            
            next_url = request.session.pop('2fa_next_url', '')
            return redirect(next_url if next_url else 'users:user_detail')
        else:
            failed_attempts += 1
            request.session[session_key] = failed_attempts
            remaining_attempts = max_attempts - failed_attempts
            
            if remaining_attempts > 0:
                messages.error(request, f'Invalid verification code. {remaining_attempts} attempt(s) remaining.')
            else:
                messages.error(request, 'Invalid verification code. No attempts remaining.')
                request.session.pop('2fa_user_id', None)
                request.session.pop('2fa_next_url', None)
                return redirect('users:login')
            
            form = TwoFactorLoginForm(user)
    else:
        form = TwoFactorLoginForm(user)
    
    context = {
        'form': form,
        'user': user,
        'remaining_attempts': remaining_attempts,
        'failed_attempts': failed_attempts,
        'max_attempts': max_attempts,
    }
    return render(request, 'users/auth/two_factor_verify.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def two_factor_setup(request):
    user = User.objects.get(id=request.user.id)
    
    if user.is_2fa_enabled:
        messages.warning(request, '2FA is already enabled for your account.')
        return redirect('users:two_factor_manage')
    
    if not user.two_fa_secret:
        user.two_fa_secret = pyotp.random_base32()
        user.save(update_fields=['two_fa_secret'])
    
    totp = pyotp.TOTP(user.two_fa_secret, interval=30)
    
    if request.method == 'POST':
        form = Enable2FAForm(user, request.POST)
        if form.is_valid():
            user.enable_2fa(user.two_fa_secret)
            
            backup_codes = user.generate_backup_codes()
            
            request.session['backup_codes'] = backup_codes
            request.session['backup_codes_shown'] = False
            
            messages.success(request, '2FA has been successfully enabled for your account!')
            return redirect('users:two_factor_backup_codes')
    else:
        form = Enable2FAForm(user)
    
    issuer = "Smart-Password-Manager-Web-"
    full_name = f"{user.full_name}".replace(" ", "-")
    uri = totp.provisioning_uri(name=full_name, issuer_name=issuer)
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    context = {
        'form': form,
        'qr_code': qr_code_base64,
        'secret': user.two_fa_secret,
        'uri': uri,
        'active_page': "2fa",
    }
    return render(request, 'users/auth/two_factor_setup.html', context)


@login_required
def two_factor_backup_codes(request):
    backup_codes = request.session.get('backup_codes', [])
    codes_shown = request.session.get('backup_codes_shown', False)
    
    if not backup_codes:
        return redirect('users:two_factor_manage')
    
    if not codes_shown:
        request.session['backup_codes_shown'] = True
    else:
        return redirect('users:two_factor_manage')
    
    context = {
        'backup_codes': backup_codes,
        'active_page': "2fa",
    }
    return render(request, 'users/auth/two_factor_backup_codes.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def two_factor_manage(request):
    user = request.user
    
    if request.method == 'POST' and 'regenerate_backup_codes' in request.POST:
        backup_codes = user.generate_backup_codes()
        request.session['backup_codes'] = backup_codes
        request.session['backup_codes_shown'] = False
        messages.success(request, 'New backup codes have been generated.')
        return redirect('users:two_factor_backup_codes')
    
    context = {
        'is_2fa_enabled': user.is_2fa_enabled,
        'has_backup_codes': bool(user.backup_codes),
        'active_page': "2fa",
    }
    return render(request, 'users/auth/two_factor_manage.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def two_factor_disable(request):
    user = request.user
    
    if not user.is_2fa_enabled:
        messages.warning(request, '2FA is not enabled for your account.')
        return redirect('users:two_factor_manage')
    
    if request.method == 'POST':
        form = Disable2FAForm(user, request.POST)
        if form.is_valid():
            user.disable_2fa()
            messages.success(request, '2FA has been disabled for your account.')
            return redirect('users:user_update')
    else:
        form = Disable2FAForm(user)
    
    context = {
        'form': form,
        'active_page': "2fa",
    }
    return render(request, 'users/auth/two_factor_disable.html', context)
