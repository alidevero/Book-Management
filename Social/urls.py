from django.urls import path
from .views import *

urlpatterns = [
    
    path("like-book/<int:book_id>/",LikeView.as_view(),name="like-book"),
    path("unlike-book/<int:book_id>/",UnlikeView.as_view(),name="unlike-book"),
    path("get-all-like/<int:book_id>/",GetAllLikeView.as_view(),name="get-all-like"),
    path("comment/",CommentView.as_view(),name="comment"),
    path("delete-comment/<int:comment_id>/",DeleteCommentView.as_view(),name="delete-comment"),
    path("update-comment/<int:comment_id>/",UpdateCommentVeiw.as_view(),name="update-comment"),
    path("get-all-comment/<int:book_id>/",GetAllComments.as_view(),name="get-all-comment"),
    path("reply-to-comment/",ReplyToCommentView.as_view(),name="reply-to-comment"),

]