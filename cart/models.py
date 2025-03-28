from django.db import models

from store.models import Product, Variation

class Cart(models.Model):
  cart_id = models.CharField(max_length=250, blank=True)
  date_added = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.cart_id
  

class CartItem(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  variations = models.ManyToManyField(Variation, blank=True)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)


  def __str__(self):
    return str(self.product) #conver self.product to string because product is a Product instance
