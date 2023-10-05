from firebase_admin import messaging #type:ignore
from .models import FCMToken
import concurrent.futures

def send_push_notification(title, body):
    print('hello send notification ')
    registration_tokens = list(FCMToken.objects.values_list('token', flat=True))
    print(registration_tokens)

    def send_message_to_token(token):
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        response = messaging.send(message)
        print(f"Successfully sent message to {token}: {response}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_message_to_token, token) for token in registration_tokens]
        
        concurrent.futures.wait(futures)

    print("All push notifications sent.")
