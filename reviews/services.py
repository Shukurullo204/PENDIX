from django.db import transaction
from .models import Review
from users.services import UserService

class ReviewService:
    @staticmethod
    def add_review(author, seller, data):
        """Добавление отзыва и мгновенный пересчет рейтинга продавца"""
        with transaction.atomic():
            review = Review.objects.create(author=author, seller=seller, **data)
            UserService.update_user_rating(seller.id) # Вызов сервиса из другого приложения
            return review
