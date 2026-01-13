from django.db.models import (
    Model,
    CharField,
    URLField,
    IntegerField,
    SlugField,
    ForeignKey,
    CASCADE,
)
from django.template.defaultfilters import slugify

MAX_NAME_LENGTH = 128
MAX_TITLE_LENGTH = 128


class Category(Model):
    name = CharField(max_length=MAX_NAME_LENGTH, unique=True)
    views = IntegerField(default=0)
    likes = IntegerField(default=0)
    slug = SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(Model):
    category = ForeignKey(Category, on_delete=CASCADE)
    title = CharField(max_length=MAX_TITLE_LENGTH)
    url = URLField()
    views = IntegerField(default=0)

    def __str__(self):
        return self.title
