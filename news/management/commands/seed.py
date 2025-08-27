import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.models import Blog  # <-- твоя модель блога из приложения news

User = get_user_model()

class Command(BaseCommand):
    help = "Generate test users, blogs and likes"

    def handle(self, *args, **kwargs):
        # Чистим старые данные
        Blog.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        # Создаём пользователей
        users = []
        for i in range(1, 7):  # 6 пользователей
            user = User.objects.create_user(
                username=f"user{i}",
                password="1234"
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS("Users created."))

        # Создаём блоги
        blogs = []
        for i in range(1, 8):  # 7 блогов
            blog = Blog.objects.create(
                header=f"Blog {i}",
                author=random.choice(users),
                public=True
            )
            blogs.append(blog)
        self.stdout.write(self.style.SUCCESS("Blogs created."))

        # Создаём лайки
        for blog in blogs:
            liked_users = random.sample(users, random.randint(1, len(users)))  # случайные лайки
            for u in liked_users:
                blog.likes.add(u)
        self.stdout.write(self.style.SUCCESS("Likes created."))

        self.stdout.write(self.style.SUCCESS("Seeding completed!"))
