from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_page, name='register'),
    path('recipes', views.add_recipes, name='recipes_add'),
    path('fridge/<int:user_id>', views.user_fridge, name='user_fridge'),
    path('product', views.product_page, name='product_page'),
    path('recipe/<int:recipe_id>', views.recipes_page, name='recipe_page'),
    path('main_page/<int:user_id>', views.main_page, name='main'),
    path('my_recipes/<int:user_id>',views.my_recipes, name='my_recipes'),
    ]
