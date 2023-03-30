from minted.models import User
from webpush import send_user_notification
from webpush.models import PushInformation

def send_push(head: str, body: str, user_id: int) -> bool:
    """
    Send a push notification to user if subscribed

    :param head: Head of notification
    :param body: Body of notification
    :param user_id: id of user
    :return: Boolean - If message was sent
    """
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

def is_user_subscribed(user_id: int) -> bool:
    """ Returns if a user is subscribed to push notifications """
    if User.objects.filter(pk=user_id).count() == 0:
        return False
    user = User.objects.get(pk=user_id)

    device = PushInformation.objects.filter(user=user).first()

    if device:
        return True
    else:
        return False
    
def unsubscribe_user_from_push(user_id: int) -> bool:
    """  Unsubscribe user from all push notifications """
    if User.objects.filter(pk=user_id).count() == 0:
        return False
    user = User.objects.get(pk=user_id)

    user_push_subscriptions = PushInformation.objects.filter(user=user)
    for subscription in user_push_subscriptions:
        subscription.delete()
    
    return True
