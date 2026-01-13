from django.shortcuts import render
from django.http import HttpRequest
from rango.models import Category, Page


def index(request: HttpRequest):
    context = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}
    context["categories"] = Category.objects.order_by("-likes")[:5]  # top 5 categories
    context["pages"] = Page.objects.order_by("-views")[:5]  # top 5 pages

    return render(request, "rango/index.html", context=context)


def about(request: HttpRequest):
    return render(
        request,
        "rango/about.html",
        context={"boldmessage": "This tutorial has been put together by Jacob."},
    )


def show_category(request: HttpRequest, category_name_slug: str):
    context = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context["category"] = category
        context["pages"] = pages
    except Category.DoesNotExist:
        context["category"] = None
        context["pages"] = None

    return render(request, "rango/category.html", context=context)
