                                               







from django.db import migrations, models











class Migration(migrations.Migration):







    dependencies = [



        ('ads', '0002_alter_ad_description'),



    ]







    operations = [



        migrations.AddField(



            model_name='ad',



            name='currency',



            field=models.CharField(choices=[('UZS', ''), ('USD', '$')], default='UZS', max_length=3, verbose_name=''),



        ),



        migrations.AlterField(



            model_name='ad',



            name='price',



            field=models.DecimalField(decimal_places=2, max_digits=15, verbose_name=''),



        ),



    ]



