from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review
from users.services import UserService

@receiver([post_save, post_delete], sender=Review)
def update_seller_rating(sender, instance, **kwargs):
    """Автоматический пересчет рейтинга при сохранении или удалении отзыва"""
    UserService.update_user_rating(instance.seller.id)
