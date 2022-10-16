from django.db import models
from django.contrib.auth.models import User

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

class Products(models.Model):
    name = models.CharField(max_length = 32)
    icon = models.CharField(max_length = 128)
    product_category = models.ForeignKey(Products_category, on_delete=models.CASCADE)

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
    cuisine_category = models.ForeignKey(Cuisine_category, on_delete=models.CASCADE)
    meal_time_category = models.ForeignKey(Meal_time_category, on_delete=models.CASCADE)
    prepare_time = models.IntegerField()
    spiciness = models.IntegerField()
    per_serving = models.IntegerField()
    is_verificated = models.BooleanField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Fridge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Fridge_products_counts(models.Model):
    product = models.ManyToManyField(Products)
    item_count = models.IntegerField()
    fridge = models.ManyToManyField(Fridge)
