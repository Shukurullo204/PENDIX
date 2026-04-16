from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from ads.models import Ad
from .services import FavoriteService

class FavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, ad_id):
        ad = Ad.objects.get(id=ad_id)
        is_favorite = FavoriteService.toggle_favorite(user=request.user, ad=ad)
        return JsonResponse({'is_favorite': is_favorite})
