from django.shortcuts import render
from django.http import HttpRequest

def index(request: HttpRequest):
    return render(request, "rango/index.html", context={ "boldmessage": "Crunchy, creamy, cookie, candy, cupcake!" })

def about(request: HttpRequest):
    return render(request, "rango/about.html", context={ "boldmessage": "This tutorial has been put together by Jacob." })