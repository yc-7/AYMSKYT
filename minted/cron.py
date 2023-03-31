from minted.models import User
from minted.notifications import send_push, is_user_subscribed
from minted.views.budget_views_functions import current_user_limit
from minted.models import Subscription
from minted.views.general_user_views.point_system_views import reward_budget_points, user_has_budget_ending_today

def send_budget_notifications(frequency: int):
	"""
	Send budget notifications to all users that are subscribed to this frequency and budgets
	
	:param frequency: The frequency of which users should be subscribed to; to receive this notification
	"""
	users = User.objects.all()
	for user in users:
		if not is_user_subscribed(user.id):
			continue
		if not user.notification_subscription:
			continue

		budget_subscription = Subscription.objects.get(name="Budgets")

		notification_subscription = user.notification_subscription
		subscriptions = notification_subscription.subscriptions.all()

		if budget_subscription not in subscriptions:
			continue

		if notification_subscription.frequency == frequency:
			budget = current_user_limit(user)

			head = "Minted"
			body = f"{budget.spent_text} for your budget, dates between ({budget.start_date})-({budget.end_date})"
			user_id = user.id

			send_push(head, body, user_id)

def send_daily_notifications():
	""" Send budget notifications to all users subscribed to daily and budget notifications """
	send_budget_notifications(frequency=1)

def send_weekly_notifications():
	""" Send budget notifications to all users subscribed to weekly and budget notifications """
	send_budget_notifications(frequency=7)

def send_monthly_notifications():
	""" Send budget notifications to all users subscribed to monthly and budget notifications """
	send_budget_notifications(frequency=30)

def give_budget_points():
	all_users = User.objects.all()
	for user in all_users:
		if user_has_budget_ending_today(user):
			reward_budget_points(user)
