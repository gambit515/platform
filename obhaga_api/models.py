from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/products/')
    description = models.TextField(max_length=1000)
    in_stock = models.BooleanField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE)