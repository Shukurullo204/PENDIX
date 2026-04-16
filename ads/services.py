from django.db import transaction
from .models import Ad, AdImage


class AdService:
    @staticmethod
    def create_ad(author, data, images=None):
        """Атомарное создание объявления и сохранение галереи изображений"""
        payload = dict(data)
        payload.pop('gallery', None)

        with transaction.atomic():
            ad = Ad.objects.create(author=author, **payload)

            if images:
                for img in images:
                    AdImage.objects.create(ad=ad, image=img)

        return ad