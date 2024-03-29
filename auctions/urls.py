from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>/<str:title>", views.listing, name="listing"),
    path("watchlist", views.watch, name="watch"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:title>", views.category, name="category")
]
