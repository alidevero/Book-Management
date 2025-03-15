from django.urls import path
from .views import *

urlpatterns = [
    path("upload-book/",UploadBookView.as_view(),name="upload-book"),
    path("view-all-book/",RetriveAllBooksView.as_view(),name="view-all-book"),
    path("view-single-book/<int:book_id>/",RetriveSingleBookView.as_view(),name="view-single-book"),
]