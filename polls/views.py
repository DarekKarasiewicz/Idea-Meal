from strenum import StrEnum  # Python 3.11 = from enum
from enum import auto

# DJANGO IMPORTS
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time

#################################################################################
#                                   FIXME
#       We should refactor all this code and start to write clean code eg:
#       `def create_shopping_list(list_of_recipes: list) -> list:`
#       That make our cleaner and easier to read also in futhure refactoring it
#       easier to understend what author thinking.
#
#################################################################################
# MODELS IMPORTS
from .models import (
    Product,
    Comment,
    Recipe,
    Fridge,
    Fridge_products_counts,
    Comments_to_Recipe,
    Recipe_products_counts,
)

# Here puts all cuisine category
class Cuisine_category(StrEnum):
    POLAND = auto()
    AMERICAN = auto()
    ASIAN = auto()

# Here puts all Meal_time_category
class Meal_time_category(StrEnum):
    BREAKFAST = auto()
    DINER = auto()
    SUPPER = auto()

# Here puts all Products_category
class Product_category(StrEnum):
    MEAT = auto()
    FISH = auto()
    DAIRY = auto()
    FRUIT = auto()
    VEGETABLES = auto()

class Product_unit(StrEnum):
    ML = auto()
    GRAMS = auto()
    UNIT = auto()

def find_recipe_base_on_products(products) -> dict:
    dict_of_recipes = {}
    list_of_recipes =[]
    all_recipes = Recipe.objects.all()
    fridge_products = {}
    for product in products:
        fridge_products[product.product.name] = product.ammount

    for recipe in all_recipes:
        products_in_recipe = Recipe_products_counts.objects.filter(recipe=recipe.id)
        for product in products_in_recipe:
            # print(f"Recipe {recipe.name} product:{product.product.name}")
            if product.product.name in fridge_products and recipe not in list_of_recipes:
                list_of_recipes.append(recipe)
    # print(list_of_recipes)

    for l_recipe in list_of_recipes:
        products_in_recipe = Recipe_products_counts.objects.filter(recipe=l_recipe.id)
        for x_product in products_in_recipe:
            if (x_product.product.name not in fridge_products.keys()):
                dict_of_recipes.setdefault(l_recipe,[]).append(x_product.product.name)

    print(dict_of_recipes)
    return dict_of_recipes

def create_shopping_list(list_of_recipes: list) -> list:
    dict_of_products = {}
    fridge_products = Fridge_products_counts.objects.all()
    for recipe in list_of_recipes:
        products = Recipe_products_counts.objects.filter(recipe=recipe.id)
        if len(products) < 1:
            raise Http404
        for product in products:
            if product.product in dict_of_products:
                dict_of_products[product.product] += product.ammount
            else:
                dict_of_products[product.product] = product.ammount
    for f_product in fridge_products:
        if f_product.product in dict_of_products:
            if (dict_of_products[f_product.product] - f_product.ammount) <= 0:
                del dict_of_products[f_product.product]

            else:
                dict_of_products[f_product.product] = (
                    dict_of_products[f_product.product] - f_product.ammount
                )

    return dict_of_products

def welcome_page(request):
    return HttpResponseRedirect("login")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("login")

def register_page(request):
    if request.method == "POST":
        login = request.POST["login"]
        password = request.POST["password"]
        email = request.POST["email"]
        if User.objects.filter(username=login).exists() == False:
            user = User.objects.create_user(login, email, password)
            user.save()
            Fridge(user=user).save()
            return HttpResponseRedirect(reverse("login"))
        else:
            return HttpResponse("400")

    return render(request, "polls/register_page.html")

def find_recipe_base_on_products(product: dict) -> Recipes:
    pass

def create_shopping_list(list_of_recipes: list) -> list:
    dict_of_products = {}
    return list_of_products

@csrf_exempt
def login_page(request):
    if request.method == "POST":
        auth_login = request.POST["auth_login"]
        auth_password = request.POST["auth_password"]
        if user := authenticate(username=auth_login, password=auth_password):
            login(request, user)
            return HttpResponseRedirect(reverse("main", args=(user.id,)))
        else:
            messages.info(request, 'Wrong password')
            # return render(request, "polls/login_page.html", {'incorrect_password':True})
    return render(request, "polls/login_page.html")

@login_required
def main_page(request, user_id):
    # TEST
    # tmp = [
    #     get_object_or_404(Recipe, pk=1),
    #     get_object_or_404(Recipe, pk=2),
    #     get_object_or_404(Recipe, pk=3),
    # ]
    if int(request.session["_auth_user_id"]) != int(user_id):
        raise Http404
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    all_recipes = Recipe.objects.all()
    all_products = Product.objects.all()

    dictionary = {}
    productIds = []

    if request.method == "POST":
        productIds = request.POST.getlist("productId[]")
        for id in productIds:
            dictionary[id] = request.POST.get("changedProducts["+ id +"]",None) 
        
    print(productIds)
    print(dictionary)
    if len(productIds) > 0:
        for id in productIds:
            product_update = Product.objects.get(id = id)
            product_update.unit = dictionary[id]
            product_update.save()


    return render(request,"polls/main_page.html",{'user':session_user
                                                 ,'recipes': all_recipes
                                                 ,'products': all_products
                                                  })

@login_required
def add_recipes(request):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    if request.method == "POST":
        name = request.POST["recipe_name"]
        description = request.POST["description"]
        difficulty = request.POST["difficulty"]
        cuisine_category = request.POST["cuisine_category"]
        meal_time_category = request.POST["meal_time_category"]
        prepare_time_post = request.POST["prepare_time"].split(":")
        prepare_time = int(prepare_time_post[0]) * 60 + int(prepare_time_post[1])
        spiciness = request.POST["spiciness"]
        per_serving = request.POST["per_serving"]
        is_verificated = False

        # YES I KNOW IT WILL WORK DIFRENTLY
        enum_cuisine_category = [
            e.value
            for e in Cuisine_category
            if str(e.value).lower() == cuisine_category.lower()
        ]
        enum_meal_time_category = [
            e.value
            for e in Meal_time_category
            if str(e.value).lower() == meal_time_category.lower()
        ]
        if len(enum_meal_time_category) == 0 and len(enum_cuisine_category) == 0:
            raise Http404

        match difficulty:
            case "easy":
                difficulty = 1
            case "medium":
                difficulty = 2
            case "hard":
                difficulty = 3
            case _:
                raise Http404

        recipes = Recipe(
            name=name,
            description=description,
            difficulty=difficulty,
            prepare_time=prepare_time,
            spiciness=spiciness,
            is_verificated=is_verificated,
            cuisine_category=enum_cuisine_category[0],
            meal_time_category=enum_meal_time_category[0],
            per_serving=per_serving,
        )
        recipes.save()
        time.sleep(2)
        return HttpResponseRedirect(reverse("main", args=(session_user.id,)))
    return render(request, "polls/recipes_page.html", {"user_id": session_user.id})

@login_required
def recipes_page(request, recipe_id):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == "POST":
        raiting = request.POST["raiting"]
        comment_text = request.POST["comment"]
        comment = Comment(raiting=raiting, description=comment_text, user=session_user)
        comment.save()
        tmf = Comments_to_Recipe(recipe=recipe, comment=comment)
        tmf.save()

    test_show = recipe.__dict__
    test_show1 = Comments_to_Recipe.objects.all()
    all_comments = []
    for x in test_show1:
        if x.recipe.id == recipe.id:
            all_comments.append(x)

    return render(
        request,
        "polls/recipe_view.html",
        {"recipe": test_show, "all_comments": all_comments, "user":session_user},
    )

@login_required
def product_page(request):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    product_category = [e.value for e in Product_category]
    print(product_category)
    if request.method == "POST":
        name = request.POST["product_name"]
        product_category_post = request.POST["product_category"]
        product_quantity = request.POST["product_quantity"]

        product = Product(name = name, product_category = product_category_post, unit = product_quantity)
        product.save()
        return HttpResponseRedirect(reverse("main", args=(session_user.id,)))

    return render(
        request,
        "polls/product_page.html",
        {"user_id": session_user.id, "product_categories": product_category},
    )

@login_required
def user_fridge(request, user_id):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    fridge = get_object_or_404(Fridge, user=session_user)
    all_products = Product.objects.all()
    # product_in_fridge = Fridge_products_counts.objects.all()
    # find_recipe_base_on_products(product_in_fridge)

    if request.method == "POST":
        product_name = request.POST["product_name"]
        product = get_object_or_404(Product, name=product_name)
        product_number = request.POST["product_number"]
        fridge_product = Fridge_products_counts(
            product=product, ammount=product_number, fridge=fridge
        )
        fridge_product.save()

    return render(
        request,
        "polls/fridge.html",
        {
            "user_id": session_user.id,
            "products": all_products,
            "product_in_fridge": product_in_fridge,
        },
    )

@login_required
def all_recipes(request):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    all_recipes = Recipe.objects.all()
    print(all_recipes)
    return render(
            request,
            "polls/all_recipes_page.html",
            {
                "all_recipes":all_recipes
            },
            )

@login_required
def my_recipes(request,user_id):
    return render(request, 'polls/my_recipes.html',{})