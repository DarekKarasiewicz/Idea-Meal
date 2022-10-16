from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse


def index(request):
    return HttpResponse("Hello world!")


@csrf_exempt
def login_page(request):
    if request.method == "POST":
        auth_login = request.POST["auth_login"]
        auth_password = request.POST["auth_password"]
        if user := authenticate(username=auth_login, password=auth_password):
            return HttpResponse("Hello World!")
        else:
            return HttpResponse("Sorry ale coś ci chyba nie poszło !")
    return render(request, "login_page.html")


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
