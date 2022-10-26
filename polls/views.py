from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Cuisine_category,Meal_time_category,Products_category,Product,Comment,Recipes,Fridge,Fridge_products_counts


def welcome_page(request):
    return HttpResponseRedirect('login')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('login')

def register_page(request):
    if request.method == "POST":
        login = request.POST["login"]
        password = request.POST["password"]
        if User.objects.filter(username=login).exists() == False:
            User.objects.create_user(login, None, password).save()
            return HttpResponseRedirect(reverse("login"))
        else:
            return HttpResponse("400")

    return render(request, "polls/register_page.html")

@csrf_exempt
def login_page(request):
    if request.method == "POST":
        auth_login = request.POST["auth_login"]
        auth_password = request.POST["auth_password"]
        if user := authenticate(username=auth_login, password=auth_password):
            login(request,user)
            return HttpResponseRedirect(reverse("main", args=(user.id,)))
        else:
            return HttpResponse("Sorry ale coś ci chyba nie poszło !")
    return render(request, "polls/login_page.html")

@login_required
def main_page(request,user_id):
    if int(request.session['_auth_user_id']) != int(user_id):
        raise Http404
    session_user = get_object_or_404(User,
                                     pk=int(request.session['_auth_user_id']))
    all_recipes = Recipes.objects.all()
    all_products = Product.objects.all()
    return render(request,"polls/main_page.html",{'name':session_user.username
                                                 ,'recipes': all_recipes
                                                 ,'products': all_products
                                                  })

@login_required
def add_recipes(request):
    session_user = get_object_or_404(User, pk=int(request.session['_auth_user_id']))
    if request.method == "POST":
        name = request.POST["recipe_name"]
        description = request.POST["description"]
        difficulty = request.POST["difficulty"]
        # cuisine_category = request.POST["cuisine_category"]
        # meal_time_category = request.POST["meal_time_category"]
        prepare_time_post = request.POST["prepare_time"].split(":")
        prepare_time = int(prepare_time_post[0])*60 + int(prepare_time_post[1])
        spiciness = request.POST["spiciness"]
        per_serving = request.POST["per_serving"]
        is_verificated = False

        match difficulty:
            case "easy":
                difficulty = 1
            case "medium":
                difficulty = 2
            case "hard":
                difficulty = 3
            case _:
                raise Http404

        recipes = Recipes(name = name
                          , description = description
                          , difficulty = difficulty
                          , prepare_time = prepare_time
                          , spiciness= spiciness
                          , is_verificated = is_verificated
                          , per_serving = per_serving
                          )
        recipes.save()
        return HttpResponseRedirect(reverse("main", args=(session_user.id,)))
    return render(request, "polls/recipes_page.html", {'user_id':
                                                       session_user.id})

@login_required
def recipes_page(request,recipe_id):
    recipe = get_object_or_404(Recipes, pk=recipe_id)
    test_show = recipe.__dict__
    return render(request, "polls/recipe_view.html", {'recipe': test_show})

def product_page(request):
    session_user = get_object_or_404(User, pk=int(request.session['_auth_user_id']))
    if request.method == "POST":
        name = request.POST["product_name"]
        product = Product(name = name)
        product.save()
        return HttpResponseRedirect(reverse("main", args=(session_user.id,)))

    return render(request, "polls/product_page.html", {'user_id':
                                                       session_user.id})

