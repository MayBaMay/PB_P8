from django.db import models
from  django.contrib.auth.models import User


class Product(models.Model):
    reference = models.CharField('Référence', max_length=100, unique=True)
    name = models.CharField('Nom', max_length=200)
    brands = models.CharField('Marque', max_length=200)
    url = models.URLField(null=True)
    image_url = models.URLField(null=True)
    image_small_url = models.URLField(null=True)
    nutrition_grade_fr = models.CharField(max_length=1)
    saturated_fat_100g = models.FloatField(null=True)
    carbohydrates_100g = models.FloatField(null=True)
    energy_100g = models.FloatField(null=True)
    sugars_100g = models.FloatField(null=True)
    sodium_100g = models.FloatField(null=True)
    salt_100g = models.FloatField(null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    reference = models.CharField('Référence', max_length=100, unique=True)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)

    def __str__(self):
        return self.reference


class Favorite(models.Model):
    created_at = models.DateTimeField("date d'envoi", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    # initial_search_product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return (self.user,self.product)
