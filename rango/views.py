from django.shortcuts import render, redirect
from django.http import HttpRequest
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def index(request: HttpRequest):
    context = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}
    context["categories"] = Category.objects.order_by("-likes")[:5]  # top 5 categories
    context["pages"] = Page.objects.order_by("-views")[:5]  # top 5 pages

    return render(request, "rango/index.html", context)


def about(request: HttpRequest):
    return render(
        request,
        "rango/about.html",
        {"boldmessage": "This tutorial has been put together by Jacob."},
    )


def show_category(request: HttpRequest, category_name_slug: str):

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
    except Category.DoesNotExist:
        category = None
        pages = None

    return render(
        request, "rango/category.html", {"category": category, "pages": pages}
    )


def add_category(request: HttpRequest):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect("/rango/")
        else:
            print(form.errors)

    return render(request, "rango/add_category.html", {"form": form})


def add_page(request: HttpRequest, category_name_slug: str):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect("/rango/")

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(
                "rango:show_category", category_name_slug=category_name_slug
            )
        else:
            print(form.errors)

    return render(
        request,
        "rango/add_page.html",
        {"form": form, "category": category},
    )
