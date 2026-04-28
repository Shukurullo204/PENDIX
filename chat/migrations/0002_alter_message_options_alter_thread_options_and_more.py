                                               







import django.db.models.deletion



import django.utils.timezone



from django.conf import settings



from django.db import migrations, models











class Migration(migrations.Migration):







    dependencies = [



        ('ads', '0010_alter_ad_options'),



        ('chat', '0001_initial'),



        migrations.swappable_dependency(settings.AUTH_USER_MODEL),



    ]







    operations = [



        migrations.AlterModelOptions(



            name='message',



            options={'ordering': ['created_at'], 'verbose_name': '', 'verbose_name_plural': ''},



        ),



        migrations.AlterModelOptions(



            name='thread',



            options={'ordering': ['-updated_at'], 'verbose_name': '', 'verbose_name_plural': ''},



        ),



        migrations.AddField(



            model_name='thread',



            name='created_at',



            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),



            preserve_default=False,



        ),



        migrations.AlterField(



            model_name='thread',



            name='ad',



            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='ads.ad'),



        ),



        migrations.AlterField(



            model_name='thread',



            name='participants',



            field=models.ManyToManyField(related_name='chat_threads', to=settings.AUTH_USER_MODEL),



        ),



    ]



