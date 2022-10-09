from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Person

@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        auth_login = (request.POST['auth_login'])
        type(auth_login)
        correct_user = Person.objects.filter(login = auth_login)
        if len(correct_user) == 0:
            return HttpResponse("Sorry ale coś ci chyba nie poszło !")
        auth_password = (request.POST['auth_password'])
        for user in correct_user:
            if user.password == auth_password:
                return HttpResponse("Hello World!")
        else:
            return HttpResponse("Sorry ale coś ci chyba nie poszło !")
    return render(request ,'login_page.html')

def index(request):
    return HttpResponse("Hello world!")
