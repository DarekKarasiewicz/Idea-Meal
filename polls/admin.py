from django.contrib import admin
# Register your models here.
from .models import Fridge, Product, Recipe, Fridge_products_counts, Comment, Recipe_products_counts

admin.site.register(Fridge)
admin.site.register(Product)
admin.site.register(Recipe)
admin.site.register(Fridge_products_counts)
admin.site.register(Comment)
admin.site.register(Recipe_products_counts)
