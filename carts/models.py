from django.db import models
from store.models import Product, Variation

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    datetime_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    cart_quantity = models.IntegerField()
    is_active = models.BooleanField(default= True)
    variations = models.ManyToManyField(Variation, blank=True)

    def sub_total(self):
        return self.product.price * self.cart_quantity

    def __unicode__(self):
        return self.product