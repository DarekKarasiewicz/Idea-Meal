from strenum import StrEnum  # Python 3.11 = from enum
from enum import auto
from datetime import datetime
from datetime import timedelta

# DJANGO IMPORTS
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

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
            if (x_product.product.name in fridge_products.keys()):
                dict_of_recipes.setdefault(l_recipe,[]).append(x_product.product.name)

    return dict_of_recipes

def filter_by_product_count(products) -> list:
    base_dict = find_recipe_base_on_products(products)
    return_dict={}

    #FIXME REMOVE recipes with None products
    all_recipes = Recipe.objects.all()
    for x_recipe in all_recipes:
        x_products = list(Recipe_products_counts.objects.filter(recipe=x_recipe.id))
        return_dict[x_recipe]=[None,1]

    for recipe, products in base_dict.items():
        ammount_of_products =len(Recipe_products_counts.objects.filter(recipe=recipe.id))
        if len(products) != ammount_of_products:
            return_dict[recipe]=[products,2]
        else:
            return_dict[recipe]=[products,3]

    return return_dict

def create_shopping_list(list_of_recipes_id: list, session_user_id: int ) -> list:
    dict_of_products = {}
    fridge_products = Fridge_products_counts.objects.all()
    for recipe_id in list_of_recipes:
        products = Recipe_products_counts.objects.filter(recipe=recipe_id)
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
    if int(request.session["_auth_user_id"]) != int(user_id):
        raise Http404
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    fridge = get_object_or_404(Fridge, user=int(request.session["_auth_user_id"]))
    fridge_products = Fridge_products_counts.objects.filter(fridge = fridge)
    all_recipes = Recipe.objects.all()

    dictionary = {}
    productIds = []

    if request.method == "POST":
        productIds = request.POST.getlist("productId[]")
        for id in productIds:
            dictionary[id] = request.POST.get("changedProducts["+ id +"]",None)

    # print(productIds)
    # print(dictionary)
    for pr in fridge_products:
        for id in productIds:
            if pr.id == int(id):
                pr.ammount = dictionary[id]
                pr.save()


            # product_update = Product.objects.get(id = id)
            # product_update.unit = dictionary[id]
            # product_update.save()

    # sorted_recipes = filter_by_product_count(all_products)
    #     sorted_recipes = ({recipe: items_in for recipe, items_in in sorted(sorted_recipes.items(), key=lambda
    #                                 item:item[1][1],reverse=True)})
    #     final_list_recipes=[]
    #     for recipe , items in sorted_recipes.items():
    #         final_list_recipes.append(recipe)

    #     return render(
    #         request,
    #         "polls/main_page.html",
    #         {"user": session_user, "recipes":filter_by_product_count(all_products), "products": all_products},
    #     )

    all_comments = Comments_to_Recipe.objects.all()
    all_comments_filtred ={}
    for comments in all_comments:
            all_comments_filtred.setdefault(comments.recipe,[]).append(comments.comment)

    return render(request,"polls/main_page.html",{'user':session_user
                                                 ,'recipes': all_recipes
                                                 ,'products': fridge_products
                                                 ,'recipes_all_comments': all_comments_filtred
                                                  })

@login_required
def add_recipes(request):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    product_unit = [e.value for e in Product_unit]

    if request.method == "POST":
        name = request.POST["recipe_name"]
        description = request.POST["description"]
        short_description = request.POST["short_description"]
        difficulty = request.POST["difficulty"]
        cuisine_category = request.POST["cuisine_category"]
        meal_time_category = request.POST["meal_time_category"]
        prepare_time_post = request.POST["prepare_time"].split(":")
        prepare_time = int(prepare_time_post[0]) * 60 + int(prepare_time_post[1])
        spiciness = request.POST["spiciness"]
        per_serving = request.POST["per_serving"]
        recipe_products = request.POST.getlist("recipe_products[][]")
        is_verificated = False

        # YES I KNOW IT WILL WORK DIFRENTLY
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
            author=session_user,
            name=name,
            description=description,
            difficulty=difficulty,
            guidance=short_description,
            prepare_time=prepare_time,
            spiciness=spiciness,
            is_verificated=is_verificated,
            cuisine_category=cuisine_category,
            meal_time_category=meal_time_category,
            per_serving=per_serving,
        )
        recipes.save()
        for product_name, product_list in product_to_recipe.items():
            new_product = Product(user=session_user, name= product_name[0], unit=
                                 product_list[0])
            new_product.save()
            recipe_product = Recipe_products_counts(product= new_product,
                                                   recipe=recipes,
                                                   ammount=product_list[1])

        return HttpResponseRedirect(reverse("main", args=(session_user.id,)))
    return render(request, "polls/recipes_page.html", {"user_id": session_user.id,"product_units": product_unit})

@login_required
def recipes_page(request, recipe_id):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    list_of_products = list(Recipe_products_counts.objects.filter(recipe=recipe.id))

    if request.method == "POST":
        raiting = request.POST["raiting"]
        comment_text = request.POST["comment"]
        comment = Comment(raiting=raiting, description=comment_text, user=session_user)
        comment.save()
        tmf = Comments_to_Recipe(recipe=recipe, comment=comment)
        tmf.save()
        return HttpResponseRedirect(reverse('recipe_page', args=[recipe_id]))

    test_show = recipe.__dict__

    all_comments_filtred = {}
    all_comments_to_recipe = Comments_to_Recipe.objects.filter(pk=recipe_id)
    for comments in all_comments_to_recipe:
            all_comments_filtred.setdefault(comments.recipe,[]).append(comments.comment)
    
    # print(all_comments_filtred)
    for x, z in all_comments_filtred.items():
        for y in z:
            print(y.raiting)

    return render(
        request,
        "polls/recipe_view.html",
        {"recipe": test_show, "all_comments_to_recipe": all_comments_filtred, "user":session_user,
         "list_of_products":list_of_products},
    )

@login_required
def product_page(request):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    product_category = [e.value for e in Product_category]
    product_unit = [e.value for e in Product_unit]
    fridge_u = get_object_or_404(Fridge, user= session_user.id)
    all_products = Fridge_products_counts.objects.filter(fridge=fridge_u.id)

    if request.method == "POST":
        name = request.POST["product_name"]
        product_category_post = request.POST["product_category"]
        product_quantity = request.POST["product_quantity"]
        product_unit = request.POST["product_unit"]

        product_exits = False
        for product in all_products:
            if product.product.name.lower() == name.lower():
                product_exits = True
        if not product_exits:
            print(product.product.name.lower())
            print(name.lower())
            new_product = Product(user= session_user,name = name, product_category = product_category_post, unit = product_unit)
            new_product.save()
            fridge = get_object_or_404(Fridge,user = session_user.id)
            new_product_fridge = Fridge_products_counts(product =new_product
                                                        , ammount=
                                                        int(product_quantity)
                                                        , fridge =fridge
                                                        )
            new_product_fridge.save()

        else:
            for product in all_products:
                if product.product.name.lower() == name.lower():
                    print(name)
                    print(product.product.name)
                    looking_product = product.product
                    print(looking_product)
            new_product = get_object_or_404(Fridge_products_counts,product=looking_product.id)
            new_product.ammount += int(product_quantity)
            new_product.save()

        return HttpResponseRedirect(reverse("main", args=(session_user.id,)))

    return render(
        request,
        "polls/product_page.html",
        {"user_id": session_user.id, "product_categories": product_category, "product_units": product_unit},
    )

@login_required
def user_fridge(request, user_id):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    fridge = get_object_or_404(Fridge, user=session_user)
    all_products = Product.objects.all()
    product_in_fridge = Fridge_products_counts.objects.all()
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
    user_recipes =[]
    if int(request.session["_auth_user_id"]) != int(user_id):
        raise Http404
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    all_recipes = Recipe.objects.all()

    for recipe in all_recipes:
        if recipe.author.id == session_user.id :
            user_recipes.append(recipe)

    if request.method == "POST":
        recipe_id = request.POST["recipeId"]
        recipe_to_delete = Recipe.objects.get(id = recipe_id)
        recipe_to_delete.delete()


    return render(request, 'polls/my_recipes.html',{"user_id": session_user.id,'recipes': user_recipes})

@login_required
def recipe_update(request,recipe_id):
    # session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))

    update_recipe = Recipe.objects.get(pk = recipe_id)

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

        update_recipe.name = name
        update_recipe.description = description
        update_recipe.difficulty = difficulty
        update_recipe.cuisine_category = cuisine_category
        update_recipe.meal_time_category = meal_time_category
        update_recipe.prepare_time = prepare_time
        update_recipe.spiciness = spiciness
        update_recipe.per_serving = per_serving

        print(name)
        print(description)
        print(difficulty)
        print(cuisine_category)
        print(meal_time_category)
        print(prepare_time)
        print(spiciness)
        print(per_serving)


        update_recipe.save()
        time.sleep(2)
        return HttpResponseRedirect(reverse("my_recipes", args=(session_user.id,)))

    return render(request, 'polls/recipe_update.html',{"recipe": update_recipe})

@login_required
def help(request):

    return render(request, 'polls/help.html',{})

@login_required
def contact(request,user_id):
    if int(request.session["_auth_user_id"]) != int(user_id):
        raise Http404
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))

    if request.method == "POST":
        message_cause = request.POST["message_cause"]
        message_title = request.POST["message_title"]
        message = request.POST["message"]
        user_email = request.POST["user_email"]
        user_name = request.POST["user_name"]

        title = message_cause + " from user "+ user_name
        email_message = render_to_string('email/email_template.html',{
            'username': user_name,
            'email': user_email,
            'message': message,
            'message_title': message_title,
        })
        # ,'s22615@pjwstk.edu.pl','s22624@pjwstk.edu.pl'
        send_mail( title ,"",'idea.meal@gmail.com',['s23202@pjwstk.edu.pl'],fail_silently=False,html_message=email_message)

    return render(request, 'polls/contact.html',{"user_id": session_user.id})

@login_required
def shopping_list(request):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))
    user_products = []

    if request.method == "POST":
        recipe_products = dict()
        user_products = dict()
        all_products = dict()
        recipes_ids = request.POST.getlist('recipes_ids[]')
        for rec_id in recipes_ids:
            i = 0
            products = Recipe_products_counts.objects.filter(recipe = rec_id).values_list('product', flat=True)
            product_amount = Recipe_products_counts.objects.filter(recipe = rec_id).values_list('ammount', flat=True)
            products = list(products)
            product_amount = list(product_amount)

            for p in products:
                some_product = get_object_or_404(Product, id = p).name
                recipe_products.update({some_product: product_amount[i]})
                i = i + 1

        print(recipe_products)
        j = 0
        fridge = get_object_or_404(Fridge, user=int(request.session["_auth_user_id"]))
        f_products = Fridge_products_counts.objects.filter(fridge = fridge).values_list('product', flat=True)
        f_amount = Fridge_products_counts.objects.filter(fridge = fridge).values_list('ammount', flat=True)
        f_products = list(f_products)
        f_amount = list(f_amount)
        for f_p in f_products:
            user_product = get_object_or_404(Product, id = f_p).name
            user_products.update({user_product: f_amount[j]})
            j = j + 1

        print(user_products)

        for r_key, r_value in recipe_products.items():
            for u_key, u_value in user_products.items():
                if r_key == u_key:
                    if r_value - u_value > 0:
                        new_amount = r_value - u_value
                        all_products.update({r_key: new_amount})
                        break
                    else:
                        break
                else:
                    all_products.update({r_key: r_value})

        print(all_products)

    return render(request,"polls/shopping_list.html",{"user_id": session_user.id})

@login_required
def contact_succes(request):
    session_user = get_object_or_404(User, pk=int(request.session["_auth_user_id"]))

    return render(request, 'polls/succes_contact.html',{"user_id": session_user})
