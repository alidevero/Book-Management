# System imports
import jwt
import os

# Third-party imports
from dotenv import load_dotenv

# Django imports
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

# Project imports
from Auth.models import *
from Auth.authentication import *
from .models import BookModel, LikeModel, CommentModel
from .serializers import *

# Load environment variables
load_dotenv()

class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, book_id):
        try:
            user = request.user
            book = get_object_or_404(BookModel, id=book_id)
            like, created = LikeModel.objects.get_or_create(user=user, book=book)
            
            if created:
                return Response(
                    {"details": "Liked successfully"},
                    status=status.HTTP_200_OK
                )
            
            return Response(
                {"details": "Already liked"},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UnlikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, book_id):
        try:
            user = request.user
            user_id = user.id
            like = LikeModel.objects.filter(user=user_id, book=book_id).first()
            
            if like:
                like.delete()
                return Response(
                    {"details": "Unliked"},
                    status=status.HTTP_200_OK
                )
            
            return Response(
                {"details": "Like not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetAllLikeView(APIView):

    def get(self, request, book_id):
        try:
            likes_of_book = LikeModel.objects.filter(book=book_id).all()
            serializer = GetAllLikes(likes_of_book, many=True)
            
            return Response(
                {"details": serializer.data},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            book_id = request.data.get('book_id')
            book = BookModel.objects.filter(id=book_id).first()
            
            if not book:
                return Response(
                    {"details": "Book not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            book_uploaded_by = book.uploaded_by
            comment = request.data.get('comment')
            serializer = CommentSerializer(data={'user': user.id, 'book': book.id, 'comment': comment})
            
            if serializer.is_valid():
                if user != book_uploaded_by:
                    serializer.save(user=user, book=book)
                    return Response(
                        {"details": "Commented successfully"},
                        status=status.HTTP_200_OK
                    )
                
                return Response(
                    {"details": "You cannot comment on your own book"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetAllComments(APIView):

    def get(self, request, book_id):
        try:            
            book_comments = CommentModel.objects.filter(book=book_id).all()
            serializer = GetAllCommentSerializer(book_comments, many=True)
            
            return Response(
                {"details": serializer.data},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ReplyToCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            book_id = request.data.get('book_id')
            comment = request.data.get('comment')
            parent = request.data.get('parent')
            
            book = BookModel.objects.filter(id=book_id).first()
            parent_comment = CommentModel.objects.filter(comment_id=parent).first()
            
            serializer = ReplyToCommentSerializer(data={
                "user": user.id, 
                "book": book.id, 
                "parent": parent_comment.comment_id, 
                "comment": comment
            })
            
            if serializer.is_valid():
                serializer.save(user=user, book=book, comment=comment)
                return Response(
                    {
                        "details": {
                            "message": "Replied Successfully",
                            "data": serializer.data
                        }
                    },
                    status=status.HTTP_200_OK
                )
            
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, comment_id):
        try:
            comment = CommentModel.objects.filter(comment_id=comment_id).first()
            
            if not comment:
                return Response(
                    {"details": "Comment not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
            user = request.user
            commented_by = comment.user
            
            if serializer.is_valid():
                if user == commented_by:
                    serializer.save()
                    return Response(
                        {"details": "Successfully updated the comment"},
                        status=status.HTTP_200_OK
                    )
                
                return Response(
                    {"details": "You are not allowed to edit someone else's comment"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, comment_id):
        try:
            comment = CommentModel.objects.filter(comment_id=comment_id).first()
            
            if not comment:
                return Response(
                    {"details": "Comment not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            comment.delete()
            return Response(
                {"details": "Deleted comment successfully"},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )