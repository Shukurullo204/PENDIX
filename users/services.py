from django.db.models import Avg

from .models import User



class UserService:

    @staticmethod

    def update_user_rating(user_id):

        ''

        user = User.objects.get(id=user_id)
        related = getattr(user, 'received_reviews', None)
        if related is None:
            user.rating = 0
            user.save(update_fields=['rating'])
            return user.rating

        avg_rating = related.aggregate(Avg('rating'))['rating__avg'] or 0

        user.rating = round(avg_rating, 2)

        user.save()

        return user.rating

