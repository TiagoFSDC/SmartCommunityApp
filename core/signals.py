# Este arquivo simula como as notificações push seriam disparadas.
# Você precisaria conectar isso no _init_.py do app 'core'.

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Registration
# from firebase_admin import messaging # Descomente quando o Firebase for configurado

@receiver(post_save, sender=Registration)
def send_registration_notification(sender, instance, created, **kwargs):
    """
    Dispara uma notificação push quando uma nova inscrição (Registration) é criada.
    """
    if created:
        event = instance.event
        volunteer = instance.volunteer
        organizer = event.organizer
        
        print(f"SINAL: Novo voluntário '{volunteer.username}' no evento '{event.title}'!")
        
        # Lógica de Notificação (Firebase Cloud Messaging)
        # (Requer que o usuário organizador tenha um FCM Token salvo no perfil)
        
        # message = messaging.Message(
        #     notification=messaging.Notification(
        #         title=f"Novo Voluntário!",
        #         body=f"{volunteer.username} acabou de se inscrever no seu mutirão: {event.title}"
        #     ),
        #     token=organizer.profile.fcm_token, # Supondo que você tenha um fcm_token
        # )
        
        # try:
        #     response = messaging.send(message)
        #     print('Notificação enviada com sucesso:', response)
        # except Exception as e:
        #     print('Erro ao enviar notificação:', e)
        pass # Fim da lógica de notificação