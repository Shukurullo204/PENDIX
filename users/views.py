from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count

from .models import User

User = get_user_model()


@require_POST
def smart_auth_view(request):
    user_login = request.POST.get('username')
    user_pass = request.POST.get('password')

    if not user_login or not user_pass:
        return JsonResponse({'status': 'error', 'message': 'Заполните все поля'}, status=400)

    user_exists = User.objects.filter(username=user_login).exists()

    if user_exists:
        user = authenticate(request, username=user_login, password=user_pass)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Вход выполнен'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Неверный пароль'}, status=401)
    else:
        new_user = User.objects.create_user(username=user_login, password=user_pass)
        login(request, new_user)
        return JsonResponse({'status': 'success', 'message': 'Аккаунт создан'})


class ProfileDetailView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_queryset(self):
        # Оптимизированный запрос для получения объявлений и отзывов
        return User.objects.prefetch_related('ads', 'reviews_received')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        # Получаем отзывы и считаем средний рейтинг
        reviews = profile.reviews_received.all().order_by('-created_at')
        context['reviews'] = reviews
        context['reviews_count'] = reviews.count()

        # Если есть отзывы, берем среднее, если нет — берем значение из поля rating модели
        avg = reviews.aggregate(Avg('rating'))['rating__avg']
        context['average_rating'] = avg if avg is not None else profile.rating

        return context


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        # ВАЖНО: используем 'phone', так как в models.py поле называется именно так
        user.username = request.POST.get('username')
        user.phone = request.POST.get('phone')

        if request.FILES.get('avatar'):
            user.avatar = request.FILES.get('avatar')

        user.save()
        return redirect('profile_detail', pk=user.pk)

    return redirect('profile_detail', pk=request.user.pk)