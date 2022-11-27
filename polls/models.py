from django.db import models
from django.contrib.auth.models import User
# from django.contrib.postgres.fields import ArrayField

class Product(models.Model):
    name = models.CharField(max_length = 32)
    product_category = models.CharField(max_length = 32)
    unit = models.IntegerField()

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

class Comments_to_Recipes(models.Model):
    recipe=models.ForeignKey(Recipes,on_delete=models.CASCADE)
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment.description

class Fridge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Fridge_products_counts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                null=False,default=None)
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE,
                               null=False,default=None)

    def __str__(self):
        return f"{self.product}:{self.item_count}"
