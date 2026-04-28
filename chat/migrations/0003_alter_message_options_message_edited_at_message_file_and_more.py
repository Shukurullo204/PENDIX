                                               







from django.db import migrations, models











class Migration(migrations.Migration):







    dependencies = [



        ('chat', '0002_alter_message_options_alter_thread_options_and_more'),



    ]







    operations = [



        migrations.AlterModelOptions(



            name='message',



            options={'ordering': ['created_at'], 'verbose_name': '', 'verbose_name_plural': ''},



        ),



        migrations.AddField(



            model_name='message',



            name='edited_at',



            field=models.DateTimeField(blank=True, null=True),



        ),



        migrations.AddField(



            model_name='message',



            name='file',



            field=models.FileField(blank=True, null=True, upload_to='chat_files/'),



        ),



        migrations.AddField(



            model_name='message',



            name='image',



            field=models.ImageField(blank=True, null=True, upload_to='chat_images/'),



        ),



        migrations.AddField(



            model_name='message',



            name='is_edited',



            field=models.BooleanField(default=False),



        ),



        migrations.AddField(



            model_name='message',



            name='status',



            field=models.CharField(choices=[('sent', ''), ('delivered', ''), ('read', '')], default='sent', max_length=10),



        ),



        migrations.AddField(



            model_name='thread',



            name='is_archived',



            field=models.BooleanField(default=False),



        ),



        migrations.AddField(



            model_name='thread',



            name='is_muted',



            field=models.BooleanField(default=False),



        ),



    ]



