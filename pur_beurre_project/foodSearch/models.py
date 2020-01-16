from django.db import models
from  django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    reference = models.CharField('Référence', max_length=100, unique=True)
    name = models.CharField('Nom', max_length=200)
    url = models.CharField(max_length=255)
    nb_products = models.IntegerField('Nombre de produits de la catégorie')

    class Meta:
        verbose_name = "catégorie"

        def __str__(self):
            return self.name


class Product(models.Model):
    reference = models.CharField('Référence', max_length=100, unique=True)
    name = models.CharField('Nom', max_length=200)
    url = models.CharField(max_length=255)
    nutrition_grade_fr = models.CharField(max_length=1)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    class Meta:
        verbose_name = "produit"

        def __str__(self):
            return self.name

# class User(models.Model):
#     name = models.CharField('Nom', max_length=200, unique=True)
#     email = models.CharField('Nom', max_length=255)
#     password = models.CharField('Nom', max_length=255)
#
#     class Meta:
#         verbose_name = "utilisateur"
#
#         def __str__(self):
#             return self.name

class Favorite(models.Model):
    created_at = models.DateTimeField("date d'envoi", auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "favoris"

        def __str__(self):
            return self.name
