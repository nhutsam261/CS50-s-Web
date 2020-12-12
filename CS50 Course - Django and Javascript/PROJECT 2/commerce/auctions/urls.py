from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("create", views.create, name="create"),
    path("listing/<int:num_id>", views.listing, name="listing"),
    path("close", views.close, name="close_view"),
    path("close/<int:num_id>", views.close, name="close"),
    path("comment/<int:num_id>", views.comment, name="comment"),
    path("addtowatchlist/<int:num_id>", views.add_to_watchlist, name="watchlist"),
    path("watchlist", views.watchlist, name="watchlist_show"),
    path("remove_from_watchlist/<int:num_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("category/<str:category>", views.category, name="category"),
    path("categories", views.categories_page, name="categories_page")
]
