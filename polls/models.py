from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Product(models.Model):
    name = models.CharField(max_length = 32)
    product_category = models.CharField(max_length = 32)
    unit = models.CharField(max_length = 32)

    def __str__(self):
        return self.name

class Comment(models.Model):
    raiting = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class Recipe(models.Model):
    name = models.CharField(max_length = 32)
    description = models.TextField()
    guidance = models.TextField(default=None)
    difficulty = models.IntegerField()
    cuisine_category = models.CharField(max_length = 32)
    meal_time_category = models.CharField(max_length = 32)
    prepare_time = models.DateTimeField(default=None, null=True)
    spiciness = models.IntegerField(null=True)
    per_serving = models.IntegerField(null=True)
    is_verificated = models.BooleanField()
    comment = models.ForeignKey(Comment,
                             on_delete=models.CASCADE,
                             null=True)

    def __str__(self):
        return self.name

class Recipe_products_counts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=False,default=None)
    ammount = models.IntegerField(default=1)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.id}){self.recipe}:{self.product}"

class Comments_to_Recipe(models.Model):
    recipe=models.ForeignKey(Recipe,on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)

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
