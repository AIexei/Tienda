from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from mptt.models import MPTTModel, TreeForeignKey
from urllib.parse import urlencode, urlunsplit
from datetime import datetime
from .storage import OverwriteStorage
from re import sub
import os
import re


def get_upload_path(instance, filename):
    file_type = filename.split('.')[-1]
    return os.path.join(datetime.now().date().strftime('%Y/%m/%d'),
                        '{}.{}'.format(sub(r'\s|\.', '', instance.stock_id), file_type))


def search_sku_by_regex(string):
    only_fields = ['name', 'manufacturer__name']
    products = list(Product.objects.select_related().only(*only_fields))

    strings = string.split(' ')
    print(strings)

    for s in strings:
        products = list(filter(lambda x: re.search(s, x.manufacturer.name + ' ' + x.name, re.IGNORECASE), products))

    skus = SKU.objects.filter(product__in=products)
    return skus


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

    def get_url(self):
        query = {'cat': self.name}
        query_string = urlencode(query)
        return urlunsplit(('', '', '/search', query_string, ''))

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name_plural = 'Products'

    OS_CHOICES = (
        ('win7', 'Windows 7'),
        ('win8', 'Windows 8'),
        ('win10', 'Windows 10'),
        ('lin', 'Linux'),
        ('mcos', 'Mac OS X'),
        ('ios', 'iOS'),
        ('and', 'Android'),
        ('winp', 'Windows phone'),
        ('blckb', 'Blackberry OS'),
        ('wtch', 'Watch OS')
        # ...
    )

    BATTERY_TYPE = (
        ('lipol', 'Li-Pol'),
        ('liion', 'Li-Ion'),
        ('nicd', 'Ni-Cd'),
        ('nimh', 'Ni-MH'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    manufacturer = models.ForeignKey(Manufacturer, related_name='products')
    categories = models.ManyToManyField(Category, related_name='products')

    os_type = models.CharField(max_length=50, choices=OS_CHOICES, null=True, blank=True)
    battery_type = models.CharField(max_length=50, choices=BATTERY_TYPE, default=None, null=True, blank=True)
    processor = models.CharField(max_length=50, default=None, null=True, blank=True)
    connectors = models.CharField(max_length=100, default=None, blank=True, null=True)

    creation_year = models.IntegerField(default=None, null=True, blank=True)
    cores_count = models.IntegerField(default=None, null=True, blank=True)
    camera = models.IntegerField(default=None, null=True, blank=True, help_text='In mega pixels')
    ram = models.IntegerField(default=None, null=True, blank=True, help_text='In gigabytes')
    builtin_memory = models.IntegerField(default=None, null=True, blank=True, help_text='In gigabytes')

    has_bluetooth = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)

    def fullname(self):
        return '{} {}'.format(self.manufacturer.name, self.name)

    def __str__(self):
        return self.name


@receiver(m2m_changed, sender=Product.categories.through)
def update_product_categories(sender, instance, **kwargs):
    action = kwargs.pop('action', None)

    if action == 'post_add' or action == 'post_remove':
        for category in instance.categories.all():
            for ancestor in category.get_ancestors():
                if ancestor not in instance.categories.all():
                    instance.categories.add(ancestor)


class Batch(models.Model):
    class Meta:
        verbose_name_plural = 'Batches'

    cost = models.IntegerField()
    count = models.IntegerField()

    def __str__(self):
        return '{}$ - {}'.format(self.cost, self.count)


class SKU(models.Model):
    class Meta:
        verbose_name_plural = 'SKUs'

    COLOR_CHOICES = (
        ('bk', 'Black'),
        ('bn', 'Brown'),
        ('be', 'Blue'),
        ('yw', 'Yellow'),
        ('rd', 'Red'),
        ('pk', 'Pink'),
        ('pe', 'Purple'),
        ('gn', 'Green'),
        ('we', 'White'),
        ('gy', 'Gray'),
        ('oe', 'Orange'),
    )

    MATERIAL_CHOICES = (
        ('pc', 'Polycarbonate'),
        ('al', 'Aluminum'),
        ('st', 'Steel'),
        ('gl', 'Glass'),
    )

    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    screen_diagonal = models.FloatField()
    screen_resolution = models.CharField(max_length=50, null=True, blank=True, help_text='Format: 640x480')
    body_material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    weight = models.IntegerField(help_text='In grams')
    battery_capacity = models.IntegerField(default=None, null=True, blank=True, help_text='In Milliamp * hour')

    likes = models.IntegerField(default=0)
    stock_id = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, related_name='skus')
    image = models.ImageField(storage=OverwriteStorage(), upload_to=get_upload_path)
    batch = models.OneToOneField(Batch, related_name='sku')

    def get_batch_status(self):
        try:
            x = self.batch
            return 1
        except:
            return 0

    def get_ppi(self):
        if self.screen_resolution:
            w, h = map(int, self.screen_resolution.split('x'))
            diagonal_in_px = (w ** 2 + h ** 2) ** 0.5
            return int(diagonal_in_px / self.screen_diagonal)

        return None

    def save(self, *args, **kwargs):
        self.stock_id = '{}  {}{}{}{}{}'.format(self.product.name, self.color, self.body_material,
                                                str(self.screen_diagonal), self.screen_resolution,
                                                str(self.weight))
        super(SKU, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(SKU, self).delete(*args, **kwargs)

    def __str__(self):
        return self.stock_id


from loginsys.models import UserProfile


class Comment(models.Model):
    class Meta:
        verbose_name_plural = 'Comments'

    owner = models.ForeignKey(UserProfile, related_name='comments')
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    sku = models.ForeignKey(SKU, related_name='comments')

    def __str__(self):
        return self.content
