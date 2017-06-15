from django.db import models
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from mptt.models import MPTTModel, TreeForeignKey
from datetime import datetime
from re import sub
import os


# Create your models here.

def get_upload_path(instance, filename):
    file_type = filename.split('.')[-1]
    return os.path.join(datetime.now().date().strftime('%Y/%m/%d'),
                        '{}.{}'.format(sub(r'\s|\.', '', instance.stock_id), file_type))


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
        #...
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

    '''
    +1. color
    +2. body material
    +3. os type
    +4. creation year
    +5. weight
    +6. screen diagonal
    +7. screen resolution
    +8. pixels per inch
    +9. camera
    +10. CPU
    +11. number of processor cores
    +12. RAM
    +13. memory
    +14. battery type
    +15. battery capacity
    +16. connectors
    +17. bluetooth
    +18. wifi
    '''

    def __str__(self):
        return self.name


@receiver(m2m_changed, sender=Product.categories.through)
def update_categories(sender, instance, **kwargs):
    action = kwargs.pop('action', None)

    if action == 'post_add' or action == 'post_remove':
        for category in instance.categories.all():
            for ancestor in category.get_ancestors():
                if ancestor not in instance.categories.all():
                    instance.categories.add(ancestor)


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
    screen_resolution = models.CharField(max_length=50)
    body_material = models.CharField(max_length=50, choices=MATERIAL_CHOICES)
    weight = models.IntegerField(help_text='In grams')
    battery_capacity = models.IntegerField(default=None, null=True, blank=True, help_text='In Milliamp * hour')

    stock_id = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, related_name='SKUs')
    image = models.ImageField(upload_to=get_upload_path)


    def get_ppi(self):
        if self.screen_resolution is not None:
            w, h = map(int, self.screen_resolution.split('x'))
            diagonal_in_px = (w**2 + h**2)**0.5
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
    date = models.DateField(auto_now_add=True)
    content = models.TextField()
    sku = models.ForeignKey(SKU, related_name='comments')

    def __str__(self):
        return self.content
