import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")

import django
django.setup()

from rango.models import Category, Page

def add_page(category: Category, title: str, url: str, views: int = 0) -> Page:
    p = Page.objects.get_or_create(category=category, title=title, url=url, views=views)[0]
    p.save()
    return p

def add_category(name: str):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

def populate():
    for category, category_data in CATEGORIES.items():
        c = add_category(category)
        for p in category_data["pages"]:
            add_page(c, p["title"], p["url"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f"- {c}: {p}")

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

CATEGORIES = {"Python": {"pages": PYTHON_PAGES},
        "Django": {"pages": DJANGO_PAGES},
        "Other Frameworks": {"pages": OTHER_PAGES}}

if __name__ == "__main__":
    print("Starting Rango population script...")
    populate()