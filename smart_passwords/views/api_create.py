import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from smart_passwords.models import SmartPassword


@login_required
@require_http_methods(["POST"])
def api_create_smart_password(request):
    try:
        data = json.loads(request.body)

        description = data.get('description', '').strip()
        length = data.get('length')
        public_key = data.get('public_key', '').strip()

        if not description:
            return JsonResponse({'error': 'Description is required'}, status=400)

        if not public_key:
            return JsonResponse({'error': 'Public key is required'}, status=400)

        try:
            length = int(length)
            if length < 12 or length > 100:
                return JsonResponse({'error': 'Length must be between 12 and 100'}, status=400)
        except (TypeError, ValueError):
            return JsonResponse({'error': 'Invalid length value'}, status=400)

        if SmartPassword.objects.filter(user=request.user, public_key=public_key).exists():
            return JsonResponse({'error': 'A password with this secret phrase already exists'}, status=400)

        smart_password = SmartPassword(
            user=request.user,
            description=description,
            length=length,
            public_key=public_key
        )
        smart_password.save()

        return JsonResponse({
            'success': True,
            'id': smart_password.id,
            'description': smart_password.description,
            'length': smart_password.length,
            'message': 'Password saved successfully!'
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
