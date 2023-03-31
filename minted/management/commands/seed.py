from django.core.management.base import BaseCommand
from faker import Faker
from django.apps import apps
from minted.models import User, Category, Expenditure, SpendingLimit, Streak, Reward
import random
import datetime

class Command(BaseCommand):

    NUMBER_OF_USERS_TO_CREATE = 10
    PASSWORD_FOR_ALL_USERS = 'Password123'
    
    CATEGORY_NAMES = ['Food', 'Transportation', 'Entertainment', 'Healthcare',
                      'Rent', 'Utilities', 'Insurance', 'Other']
    
    POINTS_START_RANGE = 10
    POINTS_END_RANGE = 200
    
    MAX_NUMBER_OF_EXPENDITURES_PER_CATEGORY = 10

    SPENDING_LIMIT_TIMEFRAMES = ['/week', '/month', '/quarter', '/year']

    NUMBER_OF_REWARDS_TO_CREATE = 5
    REWARD_CHOICES = ['qr', 'random']
    REWARD_BRAND_NAMES = ['Mesco', 'Msda', 'Mpp Store', 'Moogle Play', 'Mreggs']

    MAX_USER_STREAK = 30

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        if not self.database_is_empty():
            response = input("WARNING: The database is not empty are you sure you want to continue seeding? (Y/N): \n").lower()
            affirmatives = ['y', 'yes']
            if response not in affirmatives:
                return print("Not seeding")
            
        print("Seeding...")

        print("Creating users...")
        self.create_default_users()
        self.create_users()

        print("Creating default rewards...")
        self.create_default_rewards()

        print("Assigning friends...")
        self.assign_friends_for_users()

        print("Done!")

    def create_default_users(self):
        if not User.objects.filter(email = 'john.doe@example.org').exists():
            user = User.objects.create_user(
                    first_name = 'John',
                    last_name = 'Doe',
                    email = 'john.doe@example.org',
                    password = self.PASSWORD_FOR_ALL_USERS,
                    budget = self.create_budget(),
                    points = 100, 
                    streak_data = self.create_streak()
            )
            
        if not User.objects.filter(email = 'admin@example.org').exists():
            user = User.objects.create_superuser(
                    first_name = 'Admin',
                    last_name = 'User',
                    email = 'admin@example.org',
                    password = self.PASSWORD_FOR_ALL_USERS,
                    budget = self.create_budget(),
                    points = 0, 
                    streak_data = self.create_streak(),
            )

    def create_users(self):
        num_of_users_created = 0
        while num_of_users_created < self.NUMBER_OF_USERS_TO_CREATE:
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = f"{first_name}.{last_name}@example.org",
                password = self.PASSWORD_FOR_ALL_USERS,
                budget = self.create_budget(),
                points = random.randint(self.POINTS_START_RANGE, self.POINTS_END_RANGE), 
                streak_data = self.create_streak()
            )
            self.create_categories_and_expenditures_for_user(user)
            num_of_users_created += 1

    def create_budget(self):
        spending_limit = SpendingLimit.objects.create(
            budget = random.randint(1, 10) * 100,
            timeframe = random.choice(self.SPENDING_LIMIT_TIMEFRAMES)
        )
        return spending_limit
    
    def create_streak(self):
        streak = Streak.objects.create(
            streak = random.randint(0, self.MAX_USER_STREAK)
        )
        return streak

    def create_categories_and_expenditures_for_user(self, user):
        num_categories_to_create = random.randint(1, len(self.CATEGORY_NAMES))
        category_names = self.CATEGORY_NAMES[:num_categories_to_create]
        for category_name in category_names:
            category = Category.objects.create(
                user = user,
                name = category_name,
                budget = self.create_budget()
            )
            self.create_expenditures(category)

    def create_expenditures(self, category):
        total_expenditures_to_create = random.randint(1, self.MAX_NUMBER_OF_EXPENDITURES_PER_CATEGORY)
        num_of_created_expenditures = 0

        while num_of_created_expenditures < total_expenditures_to_create:
            expenditure = Expenditure.objects.create(
                category = category,
                title = f"{category.name}_{num_of_created_expenditures}",
                amount = random.randint(1, 100),
                date = self.faker.date_between(datetime.date(2020,1,1), datetime.date.today())
            )
            num_of_created_expenditures += 1
    
    def create_default_rewards(self):
        num_of_created_rewards = 0
        date_one_year_from_today = datetime.date.today() + datetime.timedelta(days = 365)
        while num_of_created_rewards < self.NUMBER_OF_REWARDS_TO_CREATE:
            brand_name = random.choice(self.REWARD_BRAND_NAMES)
            points_required = random.randint(1, 10) * 100

            reward = Reward.objects.create(
                brand_name = brand_name,
                points_required = points_required,
                code_type = random.choice(self.REWARD_CHOICES),
                expiry_date = self.faker.date_between(datetime.date.today(), date_one_year_from_today),
                description = f"£{points_required//100} {brand_name} voucher"
            )
            num_of_created_rewards += 1

    def assign_friends_for_users(self):
        all_users = list(User.objects.all().filter(is_superuser = False))
        for user in all_users.copy():
            all_users.remove(user)
            num_of_friends_to_add = random.randint(0, len(all_users))
            for _ in range(num_of_friends_to_add):
                user.friends.add(random.choice(all_users))

    def database_is_empty(self):
        models = apps.get_app_config('minted').get_models()
        total_object_count = 0

        for model in models:
            total_object_count += model.objects.all().count()

        return total_object_count == 0