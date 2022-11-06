from django.contrib import admin
# Register your models here.
from .models import Fridge, Product, Recipes, Fridge_products_counts

admin.site.register(Fridge)
admin.site.register(Product)
admin.site.register(Recipes)
admin.site.register(Fridge_products_counts)
