from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
            messages.info(request, 'Wrong password')
            # return render(request, "polls/login_page.html", {'incorrect_password':True})
    return render(request, "polls/login_page.html")

@login_required
def main_page(request,user_id):
    if int(request.session['_auth_user_id']) != int(user_id):
        raise Http404
    session_user = get_object_or_404(User, pk=user_id)
    # sesion_user = User.objects.filter(id=user_id)[0]
    return render(request,"polls/main_page.html",{'name':session_user.username})

def recipes(request):
    return render(request,"polls/recipes.html")


