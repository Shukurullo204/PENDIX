from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from ads.models import Ad
from .models import Thread, Message

User = get_user_model()


class ThreadListView(LoginRequiredMixin, ListView):
    template_name = 'chat/thread_list.html'
    context_object_name = 'threads'
    paginate_by = 20

    def get_queryset(self):
        return Thread.objects.filter(
            participants=self.request.user
        ).select_related('ad').prefetch_related('messages').order_by('-updated_at')


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Thread
    template_name = 'chat/chat_detail.html'
    context_object_name = 'thread'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        return Thread.objects.filter(participants=self.request.user).prefetch_related('messages')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()
        context['messages'] = thread.messages.all().order_by('created_at')
        return context


class CreateOrGetChatView(LoginRequiredMixin, View):
    """Создаёт или получает существующий диалог"""

    def get(self, request, seller_id, ad_id, *args, **kwargs):
        seller = get_object_or_404(User, id=seller_id)
        ad = get_object_or_404(Ad, id=ad_id)

        thread = Thread.objects.filter(
            ad=ad
        ).filter(participants=request.user).filter(participants=seller).first()

        if not thread:
            thread = Thread.objects.create(ad=ad)
            thread.participants.add(request.user, seller)

        return redirect('chat_detail', pk=thread.pk)