from .models import Favorite


class FavoriteService:

    @staticmethod
    def toggle_favorite(user, ad):


        favorite, created = Favorite.objects.get_or_create(user=user, ad=ad)

        if not created:
            favorite.delete()

            return False

        return True
