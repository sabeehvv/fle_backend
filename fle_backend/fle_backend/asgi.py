"""
ASGI config for fle_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter  # type:ignore
from channels.auth import AuthMiddlewareStack  # type:ignore
import chat.routing
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fle_backend.settings')

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket":
            AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))

    }
)
