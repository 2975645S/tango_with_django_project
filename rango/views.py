from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "rango/index.html", context={ "boldmessage": "Crunchy, creamy, cookie, candy, cupcake!" })

def about(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
"""Rango says here is the about page. <br/>
<a href="/rango/">Index</a>"""
    )