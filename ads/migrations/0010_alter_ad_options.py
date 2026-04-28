                                               







from django.db import migrations











class Migration(migrations.Migration):







    dependencies = [



        ('ads', '0009_alter_ad_options_alter_ad_created_at_alter_ad_price_and_more'),



    ]







    operations = [



        migrations.AlterModelOptions(



            name='ad',



            options={'ordering': ['-created_at'], 'verbose_name': '', 'verbose_name_plural': ''},



        ),



    ]



