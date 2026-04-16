from django.db.models import Avg
from .models import User

class UserService:
    @staticmethod
    def update_user_rating(user_id):
        """Пересчет среднего рейтинга пользователя на основе отзывов"""
        user = User.objects.get(id=user_id)
        avg_rating = user.received_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        user.rating = round(avg_rating, 2)
        user.save()
        return user.rating
