@run:
    python manage.py runserver

@test chapter:
    python manage.py test rango.tests_chapter{{chapter}}

@commit chapter *message:
    git add .
    git commit -m "feat({{chapter}}): {{message}}"