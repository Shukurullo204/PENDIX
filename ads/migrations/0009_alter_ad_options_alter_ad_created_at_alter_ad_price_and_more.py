                                               







from django.db import migrations, models











class Migration(migrations.Migration):







    dependencies = [



        ('ads', '0008_ad_address_ad_latitude_ad_longitude'),



    ]







    operations = [



        migrations.AlterModelOptions(



            name='ad',



            options={'verbose_name': '', 'verbose_name_plural': ''},



        ),



        migrations.AlterField(



            model_name='ad',



            name='created_at',



            field=models.DateTimeField(auto_now_add=True),



        ),



        migrations.AlterField(



            model_name='ad',



            name='price',



            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name=''),



        ),



        migrations.AlterField(



            model_name='ad',



            name='status',



            field=models.CharField(choices=[('active', ''), ('sold', ''), ('archived', '')], default='active', max_length=10),



        ),



        migrations.AlterField(



            model_name='ad',



            name='title',



            field=models.CharField(max_length=200, verbose_name=''),



        ),



    ]



