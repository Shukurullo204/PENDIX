from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ads.models import Ad
from .models import Favorite
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Ad, Favorite

@login_required
def toggle_favorite(request, ad_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Войдите в систему'}, status=403)

    ad = get_object_or_404(Ad, id=ad_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, ad=ad)

    if created:
        return JsonResponse({'status': 'added', 'message': 'Добавлено в избранное'})
    else:
        favorite.delete()
        return JsonResponse({'status': 'removed', 'message': 'Удалено из избранного'})

@login_required
def favorites_list(request):
    # Получаем все избранные записи текущего юзера
    favorites = Favorite.objects.filter(user=request.user).order_by('-id')
    return render(request, 'favorites/favorites_list.html', {'favorites': favorites})


# Пример в views.py
def ad_list(request):
    ads = Ad.objects.all()
    user_favorites = []

    if request.user.is_authenticated:
        # Получаем ID и сразу превращаем их в список целых чисел (int)
        favorites_queryset = Favorite.objects.filter(user=request.user).values_list('ad_id', flat=True)
        user_favorites = [int(fav_id) for fav_id in favorites_queryset]


    return render(request, 'ads/ad_list.html', {
        'ads': ads,
        'user_favorites': user_favorites
    })