from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

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

                                       

    threads_qs = (

        Thread.objects.filter(participants=request.user)

        .annotate(last_msg=Max('messages__created_at'))

        .order_by('-last_msg')

    )



                                            

    selected_thread_id = thread_id or request.GET.get('thread')

    active_thread = None

    if selected_thread_id:

        active_thread = get_object_or_404(Thread, id=selected_thread_id, participants=request.user)



                                         

    if request.method == 'POST' and active_thread:

        text = request.POST.get('message', '').strip()

        if text:

                                                                                  

            Message.objects.create(

                thread=active_thread,

                sender=request.user,                        

                text=text

            )



                                                                                              

            return redirect(reverse('chat_detail', kwargs={'thread_id': active_thread.id}))



                                         

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


@login_required
def thread_messages_api(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id, participants=request.user)
    after_id = request.GET.get('after_id')
    messages = thread.messages.select_related('sender').order_by('created_at')
    if after_id and after_id.isdigit():
        messages = messages.filter(id__gt=int(after_id))

    payload = []
    for msg in messages:
        payload.append({
            'id': msg.id,
            'sender': msg.sender.username,
            'sender_id': msg.sender_id,
            'text': msg.text,
            'time': msg.created_at.strftime('%H:%M'),
        })

    return JsonResponse({'messages': payload})

class CreateOrGetChatView(LoginRequiredMixin, View):

    def get(self, request, seller_id, ad_id, *args, **kwargs):

        seller = get_object_or_404(User, id=seller_id)

        ad = get_object_or_404(Ad, id=ad_id)



                                                                     

        if seller == request.user:

            return redirect('chat_list')



                                                                                           

        thread = Thread.objects.filter(ad=ad).filter(participants=request.user).filter(participants=seller).first()



        if not thread:

            thread = Thread.objects.create(ad=ad)

            thread.participants.add(request.user, seller)



                                                 

        return redirect('chat_detail', thread_id=thread.id)
