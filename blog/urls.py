from django.urls import path
from . import views

# if we have about/, both about and about/
# paths will be redirected to about/
urlpatterns = [
    path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
]