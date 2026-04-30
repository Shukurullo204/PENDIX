from django.utils import timezone
# middleware это функция которая отслеживает ваши дейстивия и считает мы его используем
# для функции "недавно" как работает? вот представим middelware таймер а функция is_online
# кнопка и эту конпку нужно нажать когда пройдет больше 5 мин вот так и работает middelware
class LastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            now = timezone.now()
            last_mark = request.session.get('last_seen_mark')
            if not last_mark or now.timestamp() - float(last_mark) >= 60:
                user.last_seen = now
                user.save(update_fields=['last_seen'])
                request.session['last_seen_mark'] = str(now.timestamp())

        return response
