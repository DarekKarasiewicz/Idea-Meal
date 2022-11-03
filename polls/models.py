from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField

class Cuisine_category(models.Model):
    name = models.CharField(max_length = 32)

    def __str__(self):
        return self.name

class Meal_time_category(models.Model):
    name = models.CharField(max_length = 32)

    def __str__(self):
        return self.name

class Products_category(models.Model):
    name = models.CharField(max_length = 32)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 32)
    product_category = models.ForeignKey(Products_category,
                                         on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    raiting = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class Recipes(models.Model):
    name = models.CharField(max_length = 32)
    description = models.TextField()
    difficulty = models.IntegerField()
    cuisine_category = models.ForeignKey(Cuisine_category,
                                         on_delete=models.CASCADE, null=True)
    meal_time_category = models.ForeignKey(Meal_time_category,
                                           on_delete=models.CASCADE, null=True)
    prepare_time = models.IntegerField(null=True)
    spiciness = models.IntegerField(null=True)
    per_serving = models.IntegerField(null=True)
    is_verificated = models.BooleanField()
    comment = models.ForeignKey(Comment,
                             on_delete=models.CASCADE,
                             null=True)

    def __str__(self):
        return self.name

class Tempomary_field(models.Model):
    recipe=models.ForeignKey(Recipes,on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)

class Fridge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Fridge_products_counts(models.Model):
    product = models.ManyToManyField(Product)
    item_count = models.IntegerField()
    fridge = models.ManyToManyField(Fridge)
