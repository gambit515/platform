from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')
    description = models.TextField(max_length=1000)
    in_stock = models.BooleanField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.name