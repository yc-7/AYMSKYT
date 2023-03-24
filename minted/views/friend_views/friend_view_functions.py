
from minted.models import Subscription


def user_is_subscribed_to_friend_notifications(user):
    friend_subscription = Subscription.objects.get(name="Friend Requests")

    notification_subscription = user.notification_subscription
    if not notification_subscription:
        return False
    subscriptions = notification_subscription.subscriptions.all()

    if friend_subscription in subscriptions:
        return True
    return False

def make_friends(user1, user2):
    user1.friends.add(user2)
    user2.friends.add(user1)