from .models import Message



from django.utils import timezone











class ChatService:



    @staticmethod



    def send_message(thread, sender, text):



        ''



        message = Message.objects.create(



            thread=thread,



            sender=sender,



            text=text,



            created_at=timezone.now()



        )







                                                        



        thread.updated_at = timezone.now()



        thread.save(update_fields=['updated_at'])







        return message

