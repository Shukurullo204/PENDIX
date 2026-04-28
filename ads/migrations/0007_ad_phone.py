                                               







from django.db import migrations, models











class Migration(migrations.Migration):







    dependencies = [



        ('ads', '0006_alter_ad_description'),



    ]







    operations = [



        migrations.AddField(



            model_name='ad',



            name='phone',



            field=models.CharField(default='', max_length=20, verbose_name=''),



            preserve_default=False,



        ),



    ]



