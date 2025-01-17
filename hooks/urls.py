from django.urls import path
from . import views

urlpatterns = [
    path('webhook', views.webhook_listener, name='webhook_listener'),
    path('sse', views.sse_endpoint, name='sse_endpoint'),
]
