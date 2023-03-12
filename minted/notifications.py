from minted.models import User
from webpush import send_user_notification
from webpush.models import PushInformation

def send_push(head, body, user_id):
    if not is_user_subscribed(user_id):
        return False
    if not (head and body and user_id):
        return False
    if User.objects.filter(pk=user_id).count() == 0:
        return False

    user = User.objects.get(pk=user_id)
    payload = {'head': head, 'body': body}
    send_user_notification(user=user, payload=payload, ttl=1000)

    return True

def is_user_subscribed(user_id):
    if User.objects.filter(pk=user_id).count() == 0:
        return False
    user = User.objects.get(pk=user_id)

    device = PushInformation.objects.filter(user=user).first()

    if device:
        return True
    else:
        return False
    
def unsubscribe_user_from_push(user_id):
    if User.objects.filter(pk=user_id).count() == 0:
        return False
    user = User.objects.get(pk=user_id)

    user_push_subscriptions = PushInformation.objects.filter(user=user)
    for subscription in user_push_subscriptions:
        subscription.delete() 