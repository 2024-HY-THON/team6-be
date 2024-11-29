# fcm.py 수정
from firebase_admin import messaging

def send_alarm_message(token, title, body):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Error sending message: {e}")
        return None
