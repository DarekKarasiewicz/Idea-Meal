from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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

    return render(request, "register_page.html")

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
    # print(user_id)
    sesion_user = User.objects.filter(id=user_id)[0]
    return render(request,"polls/main_page.html",{'name':sesion_user.username})
