from django.contrib.auth.models import AbstractUser



from django.db import models

from django.utils import timezone











class User(AbstractUser):



    phone = models.CharField(



        max_length=20,



        unique=True,



        db_index=True,



        blank=True,               



        null=True,                



        default=None              



    )



    avatar = models.ImageField(upload_to='users/avatars/', null=True, blank=True)



    location = models.CharField(max_length=255, blank=True)



    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)



    created_at = models.DateTimeField(auto_now_add=True)



    city = models.CharField(max_length=100, blank=True)

    last_seen = models.DateTimeField(null=True, blank=True)







    class Meta:



        verbose_name = ''



        verbose_name_plural = ''



    @property

    def is_online(self):

        if not self.last_seen:

            return False

        return self.last_seen >= timezone.now() - timezone.timedelta(minutes=5)



    @property

    def activity_status(self):

        return '' if self.is_online else ''

