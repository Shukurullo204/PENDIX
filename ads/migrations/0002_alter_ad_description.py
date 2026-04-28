                                               







import django.core.validators



from django.db import migrations, models











class Migration(migrations.Migration):







    dependencies = [



        ('ads', '0001_initial'),



    ]







    operations = [



        migrations.AlterField(



            model_name='ad',



            name='description',



            field=models.TextField(validators=[django.core.validators.MinLengthValidator(80, message='')], verbose_name=''),



        ),



    ]



