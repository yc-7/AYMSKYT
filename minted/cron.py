from minted.models import User
from minted.notifications import send_push, is_user_subscribed
from minted.views.budget_views_functions import current_user_limit
from minted.models import Subscription

def send_budget_notifications(frequency):
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
	send_budget_notifications(frequency=1)

def send_weekly_notifications():
	send_budget_notifications(frequency=7)

def send_monthly_notifications():
	send_budget_notifications(frequency=30)