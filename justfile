@run:
    python manage.py runserver

@test chapter:
    python manage.py test rango.tests_chapter{{chapter}}

@commit chapter *message:
    git add .
    git commit -m "feat({{chapter}}): {{message}}"

@reset:
    rm db.sqlite3
    just migrate
    python populate_rango.py
    @python manage.py createsuperuser

@migrate:
    python manage.py makemigrations rango
    python manage.py migrate