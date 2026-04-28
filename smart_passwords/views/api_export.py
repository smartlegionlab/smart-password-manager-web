from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import datetime

from smart_passwords.models import SmartPassword


@login_required
@require_http_methods(["GET"])
def api_export_passwords(request):
    try:
        passwords = SmartPassword.objects.filter(user=request.user)

        export_data = {
            "_metadata": {
                "exported_at": datetime.now().isoformat(),
                "app_name": "Smart Password Manager (Web)",
                "app_version": "v2.1.1",
                "app_type": "Web",
                "lib_name": "smartpasslib-js",
                "lib_version": "v1.0.3",
                "lib_lang": "Java Script",
                "count": passwords.count(),
            }
        }

        for pwd in passwords:
            export_data[pwd.public_key] = {
                "public_key": pwd.public_key,
                "description": pwd.description,
                "length": pwd.length
            }

        return JsonResponse(export_data, json_dumps_params={'indent': 2})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
