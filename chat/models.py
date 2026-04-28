from django.db import models

from django.conf import settings

from ads.models import Ad





class Thread(models.Model):

    ''

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='threads')

    participants = models.ManyToManyField(

        settings.AUTH_USER_MODEL,

        related_name='chat_threads'

    )

    is_archived = models.BooleanField(default=False)

    is_muted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)



    class Meta:

        ordering = ['-updated_at']

        verbose_name = ''

        verbose_name_plural = ''



    def __str__(self):

        return f"Thread for ad: {self.ad.title}"





class Message(models.Model):

    STATUS_CHOICES = [

        ('sent', ''),

        ('delivered', ''),

        ('read', ''),

    ]



    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')

    sender = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE

    )

    text = models.TextField()

    file = models.FileField(upload_to='chat_files/', null=True, blank=True)

    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')

    is_edited = models.BooleanField(default=False)

    edited_at = models.DateTimeField(null=True, blank=True)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    

    class Meta:

        ordering = ['created_at']

        verbose_name = ''

        verbose_name_plural = ''



    def __str__(self):

        return f"{self.sender.username}: {self.text[:50]}"
