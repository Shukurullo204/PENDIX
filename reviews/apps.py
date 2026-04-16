from django.apps import AppConfig

class ReviewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
    verbose_name = 'Отзывы и рейтинги'

    def ready(self):
        # Senior approach: импортируем сигналы при запуске приложения
        import reviews.signals
