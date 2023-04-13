from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=20,null=False,blank=False)
    image=models.ImageField(null=True,blank=True)
    description=models.TextField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class meta:
        db_table="category"    

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=20,null=False,blank=False)
    vender=models.CharField(max_length=20,null=False,blank=False)
    product_image=models.ImageField(null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.name        

    class meta:
        db_table="product"    

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    class Meta:
        db_table="cart"

    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price 
    
class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)  

    class Meta:
        db_table="favourite"

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=20, null=False)
    lname=models.CharField(max_length=20, null=False)
    email=models.EmailField(null=False)
    phone=models.BigIntegerField(null=False)
    address=models.TextField(null=False)
    country=models.CharField(max_length=20, null=False)
    state=models.CharField(max_length=20, null=False)
    city=models.CharField(max_length=20, null=False)
    pincode=models.CharField(max_length=6, null=False)
    
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=20,null=False)
    payment_id=models.CharField(max_length=20,null=True)
    orderstatus=(('Pending','Pending'),('Out For Shipping','Out For Shipping'),('Completed','Completed'))
    status=models.CharField(max_length=50,choices=orderstatus,default="Pending")
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=50,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True) 

    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)
    
class OrderItem(models.Model):  
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.order.id,self.order.tracking_no)
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    fname=models.CharField(max_length=20, null=False)
    lname=models.CharField(max_length=20, null=False)
    email=models.EmailField(null=False)
    phone=models.BigIntegerField(null=False)
    address=models.TextField(null=False)
    country=models.CharField(max_length=20, null=False)
    state=models.CharField(max_length=20, null=False)
    city=models.CharField(max_length=20, null=False)
    pincode=models.CharField(max_length=6, null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True) 

    def __str__(self):
        return self.user.username