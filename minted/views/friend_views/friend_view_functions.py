
from minted.models import FriendRequest, Subscription
from minted.notifications import send_push


def user_is_subscribed_to_friend_notifications(user):
    friend_subscription = Subscription.objects.get_or_create(name="Friend Requests")

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

def send_friend_request_notification(from_user, to_user):
    head = "You have received a friend request"
    body = f"{from_user} has send you a friend request"
    send_push(head, body, to_user.id)

def send_friend_request_accept_notification(to_user, from_user):
    head = "Your friend request has been accepted!"
    body = f"You and {to_user.first_name} are now friends!"
    send_push(head, body, from_user.id)