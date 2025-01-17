import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer

events = []

@csrf_exempt
async def webhook_listener(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            events.append(data)
            
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                'logger_group',
                {
                    'type': 'forward_hook',
                    'content': data
                }
            )
            
            return JsonResponse({'status': 'success', 'message': 'Data received and forwarded to WebSocket'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
