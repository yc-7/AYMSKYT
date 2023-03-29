from unittest import mock
from django.test import TestCase
from minted.models import User
from minted.views.friend_views.friend_view_functions import send_friend_request_notification
from minted.notifications import send_push

class SendFriendRequestNotificationTestCase(TestCase):

    fixtures = [
        'minted/tests/fixtures/default_user.json',
        'minted/tests/fixtures/default_other_user.json',
        "minted/tests/fixtures/default_spending_limit.json"
    ]

    def setUp(self):
        self.from_user = User.objects.get(pk=1)
        self.to_user = User.objects.get(pk=2)

    # @mock.patch('minted.notifications.send_push')
    # def test_send_friend_request_notification(self, mock_send_push):
    #     send_friend_request_notification(self.from_user, self.to_user)
    #     print(mock_send_push)
    #     print(mock_send_push.call_args_list)
    #     mock_send_push.assert_called_once_with(
    #         "You have received a friend request",
    #         f"{self.from_user} has sent you a friend request",
    #         self.to_user.id
    #     )

    # def test_send_friend_request_notification(self):
    #     with mock.patch("minted.notifications.send_push") as mock_send_push:
    #         send_friend_request_notification(self.from_user, self.to_user)
    #         print(mock_send_push)
    #         print(mock_send_push.call_args_list)
    #         # print(mock_send_push.call_args_list[0][0])
    #         mock_send_push.assert_called_once_with(
    #             "You have received a friend request",
    #             f"{self.from_user} has sent you a friend request",
    #             self.to_user.id
    #         )