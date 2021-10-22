# django_book_app

Book blog application.

# Installation:

`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py runserver`

## Admin panel:

You can access the admin panel by registering the user account and then going to `localhost8000/admin`. To register:
`python manage.py createsuperuser`

## API to get book covers:

Follow steps: https://pypi.org/project/Google-Images-Search/
When creating custom search engine, add any site to "site to search" and create the engine.
Then in "basics" tab, enable "Search the entire web" and "Image search", and remove the site
you typed inside "sites to search". "Search engine ID" is **your_api_key**.
Create `local_settings.py` inside the main directory and add the following:

```
API_KEY = __your_api_key__
CX = __your_project_cx__
```

# Project details:

## Main features:

Users can publish the books they read alongside their review (/:star:️:star:️ :star:️ :star:️ :star:️ ). Users can see the books read by other users, compare the reviews for each book, search for a book, etc. I was thinking of adding the API to get the picture of the book cover and the book description.

## Project board:

https://trello.com/b/13Ot7Zay/django

## Application built based on the tutorials by Corey Schafer

https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
