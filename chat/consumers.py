import json



from channels.generic.websocket import AsyncWebsocketConsumer



from channels.db import database_sync_to_async



from django.utils import timezone



from .models import Thread, Message



from django.contrib.auth import get_user_model







User = get_user_model()











class ChatConsumer(AsyncWebsocketConsumer):



    async def connect(self):



        self.thread_id = self.scope['url_route']['kwargs']['thread_id']



        self.user = self.scope['user']



        self.room_group_name = f'chat_{self.thread_id}'







        if not self.user.is_authenticated:

            await self.close()

            return



        is_member = await self.user_in_thread()

        if not is_member:

            await self.close()

            return



        await self.channel_layer.group_add(



            self.room_group_name,



            self.channel_name



        )



        await self.accept()







    async def disconnect(self, close_code):



        await self.channel_layer.group_discard(



            self.room_group_name,



            self.channel_name



        )







    async def receive(self, text_data):



        data = json.loads(text_data)



        message_type = data.get('type')







        if message_type == 'chat_message':



            await self.handle_message(data)



        elif message_type == 'typing':



            await self.handle_typing(data)



        elif message_type == 'mark_as_read':



            await self.handle_mark_read(data)







    async def handle_message(self, data):



        ''



        text = data.get('text', '').strip()







        if not text:



            return







        message = await self.save_message(text)

        if not message:

            return







        await self.channel_layer.group_send(



            self.room_group_name,



            {



                'type': 'chat_message',



                'message_id': message.id,



                'sender': self.user.username,

                'sender_id': self.user.id,



                'text': text,



                'timestamp': message.created_at.isoformat(),

                'time': timezone.localtime(message.created_at).strftime('%H:%M'),



                'status': 'delivered',



            }



        )







    async def handle_typing(self, data):



        ''



        await self.channel_layer.group_send(



            self.room_group_name,



            {



                'type': 'typing_indicator',



                'username': self.user.username,



                'is_typing': data.get('is_typing', True),



            }



        )







    async def handle_mark_read(self, data):



        ''



        message_id = data.get('message_id')



        await self.mark_message_read(message_id)







        await self.channel_layer.group_send(



            self.room_group_name,



            {



                'type': 'message_read',



                'message_id': message_id,



            }



        )







    async def chat_message(self, event):



        await self.send(text_data=json.dumps({



            'type': 'message',



            'data': event



        }))







    async def typing_indicator(self, event):



        await self.send(text_data=json.dumps({



            'type': 'typing',



            'username': event['username'],



            'is_typing': event['is_typing'],



        }))







    async def message_read(self, event):



        await self.send(text_data=json.dumps({



            'type': 'message_read',



            'message_id': event['message_id'],



        }))







    @database_sync_to_async



    def save_message(self, text):



                                                                   



                                                           



        try:



            thread = Thread.objects.get(id=self.thread_id)



            message = Message.objects.create(



                thread=thread,



                sender=self.user,



                text=text,



                status='delivered'                           



            )



            return message



        except Thread.DoesNotExist:



                                                          



            return None







    @database_sync_to_async



    def mark_message_read(self, message_id):



        try:



            message = Message.objects.get(id=message_id)



            message.status = 'read'



            message.is_read = True



            message.save()



        except Message.DoesNotExist:



            pass



    @database_sync_to_async

    def user_in_thread(self):

        return Thread.objects.filter(id=self.thread_id, participants=self.user).exists()

