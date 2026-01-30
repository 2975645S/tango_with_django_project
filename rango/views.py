from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime


def index(request: HttpRequest):
    context = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}
    context["categories"] = Category.objects.order_by("-likes")[:5]  # top 5 categories
    context["pages"] = Page.objects.order_by("-views")[:5]  # top 5 pages

    visitor_cookie_handler(request)
    return render(request, "rango/index.html", context)


def about(request: HttpRequest):
    context = {"boldmessage": "This tutorial has been put together by Jacob."}
    context["visits"] = request.session["visits"]

    return render(request, "rango/about.html", context)


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


@login_required
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


@login_required
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


def register(request: HttpRequest):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "rango/register.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


def user_login(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect("rango:index")
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "rango/login.html")


@login_required
def restricted(request: HttpRequest):
    return render(request, "rango/restricted.html")


@login_required
def user_logout(request: HttpRequest):
    logout(request)
    return redirect("rango:index")


def get_server_side_cookie(
    request: HttpRequest, cookie: str, default_val: str = None
) -> str:
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request: HttpRequest):
    visits = int(get_server_side_cookie(request, "visits", "1"))
    last_visit_cookie = get_server_side_cookie(
        request, "last_visit", str(datetime.now())
    )
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session["last_visit"] = str(datetime.now())
    else:
        request.session["last_visit"] = last_visit_cookie

    request.session["visits"] = visits
