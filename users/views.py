from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib import messages
from ads.models import Ad

User = get_user_model()

# 1. Умный вход (регистрация + логин)
def smart_auth_view(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        user = User.objects.filter(username=u_name).first()

        if user:
            auth_user = authenticate(username=u_name, password=p_word)
            if auth_user:
                login(request, auth_user)
                messages.success(request, 'Вы успешно зашли')
                return redirect('ad_list')
            else:
                messages.error(request, 'Неверный пароль для этого логина!')
        else:
            new_user = User.objects.create_user(username=u_name, password=p_word)
            login(request, new_user)
            messages.success(request, 'Вы успешно зашли')
            return redirect('ad_list')
    return redirect('ad_list')

# 2. Профиль пользователя
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    # Измени это имя на 'profile', чтобы оно совпадало с твоим HTML
    context_object_name = 'profile'

    def get_object(self):
        # Если в URL нет pk, показываем профиль текущего юзера
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Убедись, что фильтруешь объявления именно этого пользователя
        context['user_ads'] = Ad.objects.filter(author=self.get_object()).prefetch_related('images')
        return context
# 3. Редактирование профиля
@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.phone = request.POST.get('phone')
        if request.FILES.get('avatar'):
            user.avatar = request.FILES.get('avatar')
        user.save()
        return redirect('profile_detail', pk=user.pk)
    return redirect('profile_detail', pk=request.user.pk)