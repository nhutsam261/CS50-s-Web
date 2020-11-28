from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("create", views.create, name="create"),
    path("listing/<int:num_id>", views.listing, name="listing"),
    path("close", views.close, name="close_view"),
    path("close/<int:num_id>", views.close, name="close"),
    path("comment/<int:num_id>", views.comment, name="comment")
]
