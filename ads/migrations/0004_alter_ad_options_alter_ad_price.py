                                               







from django.db import migrations, models











class Migration(migrations.Migration):







    dependencies = [



        ('ads', '0003_ad_currency_alter_ad_price'),



    ]







    operations = [



        migrations.AlterModelOptions(



            name='ad',



            options={'ordering': ['-created_at'], 'verbose_name': '', 'verbose_name_plural': ''},



        ),



        migrations.AlterField(



            model_name='ad',



            name='price',



            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=15, verbose_name=''),



        ),



    ]



