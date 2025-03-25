from django.urls import path
from .views import *

urlpatterns = [
    path("upload-book/",UploadBookView.as_view(),name="upload-book"),
    path("view-all-book/",RetriveAllBooksView.as_view(),name="view-all-book"),
    path("view-single-book/<int:book_id>/",RetriveSingleBookView.as_view(),name="view-single-book"),
    path("delete-book/<int:book_id>/",DeleteBookView.as_view(),name="delete-book"),
    path("update-book/<int:book_id>/",UpdateBookView.as_view(),name="update-book"),
]