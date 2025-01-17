import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
import time
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

def sse_endpoint(request):
    def event_stream():
        while True:
            if events:  # Check if there are new events
                event = events.pop(0)  # Get the oldest event
                yield f"data: {json.dumps(event)}\n\n"  # Send as SSE
            time.sleep(1)  # Delay to prevent excessive CPU usage

    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
