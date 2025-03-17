from django.urls import path
from .views import *

urlpatterns = [
    
    path("like-book/<int:book_id>/",LikeView.as_view(),name="like-book"),
    path("get-all-like/<int:book_id>/",GetAllLikeView.as_view(),name="get-all-like"),
    path("comment/",CommentView.as_view(),name="comment"),
    path("get-all-comment/<int:book_id>/",GetAllComments.as_view(),name="get-all-comment"),
    path("reply-to-comment/",ReplyToCommentView.as_view(),name="reply-to-comment"),

]