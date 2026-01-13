from django.forms import ModelForm, CharField, IntegerField, HiddenInput, URLField
from rango.models import Category, Page, MAX_NAME_LENGTH, MAX_TITLE_LENGTH


class CategoryForm(ModelForm):
    name = CharField(
        max_length=MAX_NAME_LENGTH, help_text="Please enter the category name."
    )
    views = IntegerField(widget=HiddenInput(), initial=0)
    likes = IntegerField(widget=HiddenInput(), initial=0)
    slug = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ("name",)


class PageForm(ModelForm):
    title = CharField(
        max_length=MAX_TITLE_LENGTH, help_text="Please enter the title of the page."
    )
    url = URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = IntegerField(widget=HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ("category",)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")

        if url and not url.startswith("http://"):
            url = f"http://{url}"
            cleaned_data["url"] = url

        return cleaned_data
