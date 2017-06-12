from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Product(models.Model):
    class Meta:
        verbose_name_plural = 'Products'

    name = models.CharField(max_length=100)
    description = models.TextField()
    count = models.IntegerField(default=0)
    #..................

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100, unique=True)
    root = models.ForeignKey('self', blank=True)
    subcategories = ArrayField(models.ForeignKey('self'))
    #..............

    def __str__(self):
        return self.name


class Comment(models.Model):
    class Meta:
        verbose_name_plural = 'Comments'

    owner = models.ForeignKey #..............
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    product = models.ForeignKey(Product)


    def __str__(self):
        return self.content



