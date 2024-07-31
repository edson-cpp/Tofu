from django.db import models
from stdimage.models import StdImageField
from django.db.models import signals
from django.template.defaultfilters import slugify

class Base(models.Model):
    created = models.DateField('Creation date', auto_now_add=True)
    modified = models.DateField('Update date', auto_now=True)
    active = models.BooleanField('Active?', default=True)
    class Meta:
        abstract = True

class Product(Base):
    name = models.CharField('Name', max_length=100)
    price = models.DecimalField('Price', decimal_places=2, max_digits=10)
    image = StdImageField('Image', upload_to='product', variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.name
    
def product_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.name)

signals.pre_save.connect(product_pre_save, sender=Product)

class Client(Base):
    name = models.CharField('Name', max_length=100)
    surname = models.CharField('Surname', max_length=100)
    email = models.EmailField('E-mail', max_length=100)
