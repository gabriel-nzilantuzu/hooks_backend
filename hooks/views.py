import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer

# A function for returning JsonResponse (sync, since JsonResponse itself isn't async-safe)
def json_response(data, status=200):
    return JsonResponse(data, status=status)

@csrf_exempt
async def webhook_listener(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                'logger_group',
                {
                    'type': 'forward_hook',
                    'content': data,
                }
            )
            return json_response({'status': 'success', 'message': 'Data received and forwarded to WebSocket'})
        except json.JSONDecodeError:
            return json_response({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return json_response({'status': 'error', 'message': 'Invalid method'}, status=405)
