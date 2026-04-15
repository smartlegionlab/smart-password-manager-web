import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from smart_passwords.models import SmartPassword


@login_required
@require_http_methods(["POST"])
def api_import_passwords(request):
    try:
        data = json.loads(request.body)

        added = 0
        skipped = 0
        invalid = 0

        if "_metadata" in data:
            metadata = data.pop("_metadata")
            print(f"Import metadata: device={metadata.get('device_type', 'unknown')}, "
                  f"app={metadata.get('app_version', 'unknown')}, "
                  f"lib={metadata.get('lib_version', 'unknown')}")

        for public_key, entry in data.items():
            if not isinstance(entry, dict):
                invalid += 1
                continue

            description = entry.get('description', '').strip()
            length = entry.get('length')
            stored_public_key = entry.get('public_key', '')

            if not description or not stored_public_key:
                invalid += 1
                continue

            if stored_public_key != public_key:
                invalid += 1
                continue

            try:
                length = int(length)
                if length < 12 or length > 100:
                    invalid += 1
                    continue
            except (TypeError, ValueError):
                invalid += 1
                continue

            if SmartPassword.objects.filter(user=request.user, public_key=public_key).exists():
                skipped += 1
                continue

            SmartPassword.objects.create(
                user=request.user,
                description=description,
                length=length,
                public_key=public_key
            )
            added += 1

        return JsonResponse({
            'success': True,
            'added': added,
            'skipped': skipped,
            'invalid': invalid,
            'total': added + skipped + invalid
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
