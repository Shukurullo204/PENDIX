from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.db.models import Max
from django.urls import reverse
from ads.models import Ad
from .models import Thread, Message

User = get_user_model()

@login_required
def chat_view(request, thread_id=None):
    # 1. Получаем все чаты пользователя
    threads_qs = (
        Thread.objects.filter(participants=request.user)
        .annotate(last_msg=Max('messages__created_at'))
        .order_by('-last_msg')
    )

    # 2. Определяем, какой чат сейчас открыт
    selected_thread_id = thread_id or request.GET.get('thread')
    active_thread = None
    if selected_thread_id:
        active_thread = get_object_or_404(Thread, id=selected_thread_id, participants=request.user)

    # 3. ЛОГИКА ОТПРАВКИ СООБЩЕНИЯ (POST)
    if request.method == 'POST' and active_thread:
        text = request.POST.get('message', '').strip()
        if text:
            # Мы берем request.user — это тот, кто СЕЙЧАС нажал кнопку "Отправить"
            Message.objects.create(
                thread=active_thread,
                sender=request.user,  # Именно текущий юзер!
                text=text
            )

            # Редирект, чтобы сообщение не отправилось второй раз при обновлении страницы (F5)
            return redirect(reverse('chat_detail', kwargs={'thread_id': active_thread.id}))

    # 4. Собираем данные для списка чатов
    thread_rows = []
    for t in threads_qs:
        thread_rows.append({
            'thread': t,
            'other_user': t.participants.exclude(id=request.user.id).first(),
            'last_message': t.messages.last()
        })

    context = {
        'threads': thread_rows,
        'active_thread': active_thread,
        'active_other_user': active_thread.participants.exclude(id=request.user.id).first() if active_thread else None,
        'messages': active_thread.messages.all().order_by('created_at') if active_thread else [],
    }
    return render(request, 'chat/chat.html', context)
class CreateOrGetChatView(LoginRequiredMixin, View):
    def get(self, request, seller_id, ad_id, *args, **kwargs):
        seller = get_object_or_404(User, id=seller_id)
        ad = get_object_or_404(Ad, id=ad_id)

        # Проверяем, не пытается ли пользователь написать самому себе
        if seller == request.user:
            return redirect('chat_list')

        # Ищем существующий чат именно между этими двумя пользователями по этому объявлению
        thread = Thread.objects.filter(ad=ad).filter(participants=request.user).filter(participants=seller).first()

        if not thread:
            thread = Thread.objects.create(ad=ad)
            thread.participants.add(request.user, seller)

        # ВАЖНО: Редиректим на конкретный ID чата
        return redirect('chat_detail', thread_id=thread.id)