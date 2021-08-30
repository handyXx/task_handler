import random

import faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

from blog.models import Category, Task


class Command(BaseCommand):
    help = "Data Generator"

    def handle(self, *args, **options):

        fake = Faker()

        qs_category_num = Category.objects.all().count()

        self.stdout.write(self.style.SUCCESS(f"Start insering data  in category model"))
        for _ in range(qs_category_num + 1, qs_category_num + 16):
            uid = random.randint(1, 4)
            user_inst = User.objects.get(id=uid)
            name = fake.text(max_nb_chars=30)
            Category.objects.create(name=name, user=user_inst)
        qs_category_num = Category.objects.all().count()
        self.stdout.write(
            self.style.SUCCESS(f"{qs_category_num} inserted row in category model")
        )

        self.stdout.write(self.style.SUCCESS(f"Start insering data  in Task model"))
        for _ in range(20):
            name = fake.text(max_nb_chars=30)
            desc = fake.text(max_nb_chars=270)
            uid = random.randint(1, 4)
            user_inst = User.objects.get(id=uid)
            gid = random.randint(1, qs_category_num)
            g_inst = Category.objects.get(id=gid)

            Task.objects.create(
                name=name,
                user=user_inst,
                description=desc,
                price=(round(random.uniform(9.99, 99.99), 2)),
                category=g_inst,
            )
        self.stdout.write(self.style.SUCCESS(f"Finished inserting data in Task model"))
