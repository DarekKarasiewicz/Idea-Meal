from django.contrib import admin
# Register your models here.
from .models import Fridge, Product, Recipes, Fridge_products_counts, Cuisine_category, Meal_time_category, Products_category, Comment

admin.site.register(Fridge)
admin.site.register(Product)
admin.site.register(Recipes)
admin.site.register(Fridge_products_counts)
admin.site.register(Cuisine_category)
admin.site.register(Comment)
admin.site.register(Products_category)
admin.site.register(Meal_time_category)
