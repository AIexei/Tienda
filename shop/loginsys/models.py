from django.db import models
from django.contrib.auth.models import User
from products.models import SKU

# Create your models here.

class UserProfile(models.Model):
    class Meta:
        verbose_name_plural = 'User profiles'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    favourites = models.ManyToManyField(SKU, related_name='amateurs', blank=True)

    def __str__(self):
        return self.user.username