from django.db import models
from django.urls import reverse
from category.models import Category

class Product(models.Model):
  product_name = models.CharField(max_length=200, unique=True)
  slug = models.SlugField(max_length=200, unique=True)
  description = models.TextField(max_length=500, blank=True)
  price = models.IntegerField()
  image = models.ImageField(upload_to='photo/products')
  stock = models.IntegerField()
  is_available = models.BooleanField(default=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ['-created_date']


  def get_url (self):
    return reverse('product_detail', args=[self.category.slug, self.slug])

  def __str__(self):
    return self.product_name



class VariationManager(models.Manager):
  def colors(self):
    return super(VariationManager, self).filter(variation_category='color', is_active=True)
  
  def sizes(self):
    return super(VariationManager, self).filter(variation_category='size', is_active=True)
  


class Variation(models.Model):
  variation_category_choices = {
    ('color', 'color'),
    ('size', 'size')
  }
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  variation_category = models.CharField(max_length=50, choices=variation_category_choices)
  variation_value = models.CharField(max_length=50)
  is_active = models.BooleanField(default=True)
  created_date = models.DateTimeField(auto_now_add=True)


  objects = VariationManager()

  class Meta:
    unique_together= ('product', 'variation_value')

  def __str__(self):
    return f"{self.product} {self.variation_value}"