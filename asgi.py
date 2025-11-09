"""
Configuração ASGI para o projeto mutirao_project.

Expõe o ASGI callable como uma variável de nível de módulo chamada `application`.
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# É crucial configurar o settings antes de importar qualquer coisa do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mutirao_project.settings')
django.setup()

# Importar routing depois do setup()
import core.routing

# Esta é a aplicação ASGI principal
application = ProtocolTypeRouter({
    # Requisições HTTP/HTTPS tradicionais
    "http": get_asgi_application(),

    # Conexões WebSocket
    "websocket": AuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
})