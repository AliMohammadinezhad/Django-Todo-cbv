from django.core.management.base import BaseCommand
from faker import Faker

from accounts.models import User
from ...models import Todo


class Command(BaseCommand):
    help = "inserting some dummy Data!"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **kwargs):
        user = User.objects.create_user(
            username=self.fake.user_name(),
            password=self.fake.password(),
            email=self.fake.email(),
        )
        
        for _ in range(5):
            Todo.objects.create(
                user=user,
                name=self.fake.sentence(),
                status=self.fake.boolean(),
            )
        
