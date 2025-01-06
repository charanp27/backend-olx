from django.db import models
# from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from django.utils import timezone
# class User(AbstractUser):
#     first_name = models.CharField(max_length=255, blank=True)
#     last_name = models.CharField(max_length=255, blank=True)
#     email = models.EmailField(unique=True)

#     def __str__(self):
#         return self.username

#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         help_text='The groups this user belongs to.',
#         related_name='demo_users'  # Customize the reverse accessor name
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         related_name='demo_users'  # Customize the reverse accessor name
#     )

class Category(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="brands", null=True,  
        blank=True )  
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_pic = models.CharField(max_length=1000000)
    created_at = models.DateTimeField(auto_now_add=True)  
    likes = models.ManyToManyField(User, related_name='liked_products', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.like_count = self.likes.count()
        super().save(*args, **kwargs)
    

class yearlyProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='yearly_sales')
    year = models.IntegerField()
    sales = models.IntegerField(help_text="Number of products sold in the year")

    def __str__(self):
        return f"{self.product.name} ({self.year})"

class AreaWiseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='area_wise_availability')
    area = models.CharField(max_length=200)
    quantity = models.IntegerField(help_text="Quantity available in this area")

    def __str__(self):
        return f"{self.product.name} - {self.area}"
    
# class Wishlist(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist') 
#     products = models.ManyToManyField('Product', blank=True) 
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"