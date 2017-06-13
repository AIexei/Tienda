from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from datetime import datetime
import os


# Create your models here.

def get_upload_path(instance, filename):
    return os.path.join(datetime.now().date().strftime('%Y/%m/%d'), filename)


class Manufacturer(models.Model):
    class Meta:
        verbose_name_plural = 'Manufacturers'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(MPTTModel):
    class Meta:
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name_plural = 'Products'

    OS_CHOICES = (
        ('win', 'Windows'),
        ('lin', 'Linux'),
        ('mac', 'MacOS'),
        ('ios', 'iOS'),
        ('and', 'Android'),
        ('win_p', 'Windows phone'),
        ('blb', 'BlackberryOS'),
        #...
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.ForeignKey(Manufacturer, related_name='products')
    categories = models.ManyToManyField(Category, related_name='products')
    creation_year = models.IntegerField()
    weight = models.IntegerField()
    has_bluetooth = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    os_type = models.CharField(max_length=50, choices=OS_CHOICES)


    def __str__(self):
        return self.name


class SKU(models.Model):
    class Meta:
        verbose_name_plural = 'SKUs'

    COLOR_CHOICES = (
        ('bc', 'black'),
        ('bn', 'brown'),
        ('be', 'blue'),
        ('yw', 'yellow'),
        ('rd', 'red'),
        ('pk', 'pink'),
        ('gn', 'green'),
        ('we', 'white'),
        ('gy', 'gray'),
        ('oe', 'orange'),
    )

    MATERIAL_CHOICES = (
        ('pc', 'polycarbonate'),
        ('al', 'aluminum'),
        ('st', 'steel'),
        ('gl', 'glass'),
    )

    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    diagonal = models.FloatField()
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    product = models.ForeignKey(Product, related_name='SKUs')
    image = models.ImageField(upload_to=get_upload_path)

    def __str__(self):
        return '{}  {}{}{}'.format(self.product.name, self.color, self.material, str(self.diagonal))


from loginsys.models import UserProfile


class Comment(models.Model):
    class Meta:
        verbose_name_plural = 'Comments'

    owner = models.ForeignKey(UserProfile, related_name='comments')
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    product = models.ForeignKey(Product, related_name='comments')

    def __str__(self):
        return self.content