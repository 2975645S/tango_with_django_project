from django.contrib import admin
from rango import models

TO_REGISTER = [models.Category, models.Page]

for model in TO_REGISTER:
    admin.site.register(model)