from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from smart_passwords.forms.smart_password_update import SmartPasswordUpdateForm
from smart_passwords.models import SmartPassword


@login_required
def smart_password_update_view(request, pk):
    smart_password = get_object_or_404(SmartPassword, pk=pk)
    form = SmartPasswordUpdateForm(request.POST or None, instance=smart_password)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'The data for the smart password "{smart_password.description}" has been updated successfully!')
            return redirect('smart_passwords:smart_password_list')

    context = {
        'form': form,
        'active_page': 'manager',
    }
    
    return render(request, 'smart_passwords/smart_password_update.html', context)
