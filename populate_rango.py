import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")

import django
django.setup()

from rango.models import Category, Page

def add_page(category: Category, title: str, url: str, views: int = 0) -> Page:
    p = Page.objects.get_or_create(category=category, title=title, url=url, views=views)[0]
    p.save()
    return p

def add_category(name: str, views: int = 0, likes: int = 0) -> Category:
    c = Category.objects.get_or_create(name=name, views=views, likes=likes)[0]
    c.save()
    return c

def populate():
    for category, c_data in CATEGORIES.items():
        c = add_category(category, c_data["views"], c_data["likes"])
        for p_data in c_data["pages"]:
            add_page(c, p_data["title"], p_data["url"])

    for c in Category.objects.all():
        for p_data in Page.objects.filter(category=c):
            print(f"- {c}: {p_data}")

PYTHON_PAGES = [
    {"title": "Official Python Tutorial",
     "url":"http://docs.python.org/3/tutorial/"},
    {"title":"How to Think like a Computer Scientist",
     "url":"http://www.greenteapress.com/thinkpython/"},
    {"title":"Learn Python in 10 Minutes",
     "url":"http://www.korokithakis.net/tutorials/python/"}
]

DJANGO_PAGES = [
    {"title":"Official Django Tutorial",
     "url":"https://docs.djangoproject.com/en/2.1/intro/tutorial01/"},
    {"title":"Django Rocks",
     "url":"http://www.djangorocks.com/"},
    {"title":"How to Tango with Django",
     "url":"http://www.tangowithdjango.com/"}
]

OTHER_PAGES = [
    {"title":"Bottle",
     "url":"http://bottlepy.org/docs/dev/"},
    {"title":"Flask",
     "url":"http://flask.pocoo.org"}
]

CATEGORIES = {"Python": {"pages": PYTHON_PAGES, "views": 128, "likes": 64},
        "Django": {"pages": DJANGO_PAGES, "views": 64, "likes": 32},
        "Other Frameworks": {"pages": OTHER_PAGES, "views": 32, "likes": 16}}

if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()