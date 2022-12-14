from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Product(models.Model):
    name = models.CharField(max_length = 32, default=None)
    product_category = models.CharField(max_length = 32, default=None)
    unit = models.CharField(max_length = 32, default=None)

    def __str__(self):
        return self.name

class Comment(models.Model):
    raiting = models.IntegerField(default=None)
    description = models.TextField(default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.description

class Recipe(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,null=True,default=None)
    name = models.CharField(max_length = 32, default=None)
    description = models.TextField(default=None)
    guidance = models.TextField(default=None)
    difficulty = models.IntegerField(default=None)
    cuisine_category = models.CharField(max_length = 32, default=None)
    meal_time_category = models.CharField(max_length = 32, default=None)
    prepare_time = models.DateTimeField(default=None, null=True)
    spiciness = models.IntegerField(null=True, default=None)
    per_serving = models.IntegerField(null=True, default=None)
    is_verificated = models.BooleanField(default=None)
    comment = models.ForeignKey(Comment,
                             on_delete=models.CASCADE,
                             null=True, default=None)

    def __str__(self):
        return self.name

class Recipe_products_counts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=False,default=None)
    ammount = models.IntegerField(default=1)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"({self.id}){self.recipe}:{self.product}"

class Comments_to_Recipe(models.Model):
    recipe=models.ForeignKey(Recipe,on_delete=models.CASCADE, default=None)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.comment.description

class Fridge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Fridge_products_counts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=False,default=None)
    ammount = models.IntegerField(default=1)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE,
                               null=False,default=None)

    def __str__(self):
        return f"{self.product}:{self.ammount}"
