from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_view, name='logout_view'),
    path('register', views.register_page, name='register'),
    path('main_page/<int:user_id>', views.main_page, name='main'),
    ]
