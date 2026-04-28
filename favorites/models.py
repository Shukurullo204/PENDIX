from django.db import models



from django.contrib.auth import get_user_model



from ads.models import Ad







User = get_user_model()







class Favorite(models.Model):



    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')



    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='favorited_by')



    created_at = models.DateTimeField(auto_now_add=True)







    class Meta:



        unique_together = ('user', 'ad')                                                 



        verbose_name = ''



        verbose_name_plural = ''







    def __str__(self):



        return f"{self.user.username} -> {self.ad.title}"

