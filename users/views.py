from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib import messages
from ads.models import Ad


User = get_user_model()

# Умный вход регистрация + логин
def smart_auth_view(request):
    # тут узнаем зашел ли в страницу с регистрацией
    if request.method == 'POST':
        # если он отправлил форму (логин и пароль)
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        # то тут получаем то что он отправил
        user = User.objects.filter(username=u_name).first()
        # и потом ищё в бд кто первый отправил
        if user:
            auth_user = authenticate(username=u_name, password=p_word)
            # тут с помощью authenticate берет сырой пароль (p_word) потом делает его в хеш (фарш) потом
            # идет в бд сравнить с тем хешем который лежит
            if auth_user:
                login(request, auth_user)
                messages.success(request, 'Вы успешно зашли')
                return redirect('ad_list')
            # если всё совпадает то выкидывает в ('ad_list')
            else:
                messages.error(request, 'Неверный пароль для этого логина!')
        else:
            # тут создаем пользователя если такого логина нет в бд
            new_user = User.objects.create_user(username=u_name, password=p_word)
            login(request, new_user)
            messages.success(request, 'Вы успешно зашли')
            return redirect('ad_list')
    return redirect('ad_list')

# профиль пользователя
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Если в URL нет pk, показываем профиль текущего юзера
        # pk-это нужно чтобы можно было видить другие профили и в сайте будет отображаться вместо pk его id
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_ads'] = Ad.objects.filter(author=self.get_object()).prefetch_related('images')
        return context
    # тут мы используем prefetch_related почему? чтобы оптимизировать сайт и не нагружать бд
    # спросите как работает? то просто тут передается 2 запроса первый дать все объявления
    # второй дать все фотки а без него было бы так за каждое фото из объявления было бы 1 запрос
    # а с prefetch_related только 1 дать все а не по одному

# редактирование профиля
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
# мы тут просто получаем всё из бд потом его передаем измененный обратно



