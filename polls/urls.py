from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_page, name='login'),
    path('register', views.register_page, name='register'),
    path('main_page/<int:user_id>', views.main_page, name='main'),
    ]
