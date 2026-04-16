from .models import Favorite

class FavoriteService:
    @staticmethod
    def toggle_favorite(user, ad):
        """Добавить в избранное, если нет, или удалить, если уже есть"""
        favorite, created = Favorite.objects.get_or_create(user=user, ad=ad)
        if not created:
            favorite.delete()
            return False # Удалено
        return True # Добавлено
