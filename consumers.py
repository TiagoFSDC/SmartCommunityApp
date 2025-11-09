import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Event
# NOTA: Para uma autenticação JWT em Consumers, é necessário um middleware customizado,
# pois o AuthMiddlewareStack padrão do Django usa Sessões.
# Para simplificar, este exemplo focará na lógica do chat.

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        """
        Chamado quando um cliente tenta se conectar ao WebSocket.
        """
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.event_group_name = f'chat_event_{self.event_id}'
        
        # TODO: Adicionar validação de autenticação (JWT) aqui.
        # Por enquanto, apenas aceita a conexão.
        
        # Verifica se o evento existe
        if not await self.event_exists(self.event_id):
            await self.close()
            return

        # Entra no grupo (sala) do Channel Layer
        await self.channel_layer.group_add(
            self.event_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"WS: Conexão aceita para o evento {self.event_id}")

    async def disconnect(self, close_code):
        """
        Chamado quando a conexão é fechada.
        """
        # Sai do grupo (sala)
        await self.channel_layer.group_discard(
            self.event_group_name,
            self.channel_name
        )
        print(f"WS: Conexão fechada para o evento {self.event_id}")

    async def receive(self, text_data):
        """
        Recebe uma mensagem do cliente (WebSocket).
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # TODO: Pegar o usuário autenticado (self.scope['user'])
        username = "UsuárioAnônimo" # Substituir pelo usuário real
        
        print(f"WS: Mensagem recebida no evento {self.event_id}: {message}")

        # Envia a mensagem para o grupo (sala)
        await self.channel_layer.group_send(
            self.event_group_name,
            {
                'type': 'chat_message', # Chama a função 'chat_message'
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        """
        Função chamada pelo 'group_send' para enviar a mensagem
        de volta para todos os clientes no grupo.
        """
        message = event['message']
        username = event['username']

        # Envia a mensagem de volta para o cliente (WebSocket)
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def event_exists(self, event_id):
        """
        Verifica se um evento existe no banco de dados de forma assíncrona.
        """
        return Event.objects.filter(id=event_id).exists()