from django.db.models import Model, CharField, URLField, IntegerField, ForeignKey, CASCADE

class Category(Model):
    name = CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Page(Model):
    category = ForeignKey(Category, on_delete=CASCADE)
    title = CharField(max_length=128)
    url = URLField()
    views = IntegerField(default=0)

    def __str__(self):
        return self.title