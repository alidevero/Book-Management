# System imports
import os
import jwt

# Third-party imports
from dotenv import load_dotenv

# Django imports
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, permissions

# Project imports
from Auth.models import *
from Auth.authentication import *
from .models import BookModel
from .serializers import *

# Load environment variables
load_dotenv()

class UploadBookView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        authentication_classes = [JWTAuthentication]
        permission_classes = [permissions.IsAuthenticated]
        
        try:    
            user = request.user
            serializer = UploadBookSerializer(data=request.data)
            if serializer.is_valid():
                # Assign the authenticated user to 'uploaded_by'
                serializer.save(uploaded_by = user)
                
                return Response(
                    {"details": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            
            return Response(
                {"details": serializer.errors}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong in upload book view"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RetriveAllBooksView(APIView):

    def get(self , request):
        try:  
            books = BookModel.objects.all()
            serializer = ViewAllBooks(books, many = True)
            return Response(
                {"details": serializer.data},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Error while getting books"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RetriveSingleBookView(APIView):
    
    def get(self , request, book_id):
        try:
            book_instance = get_object_or_404(BookModel, id = book_id)
            serializer = ViewSingleBookSerializer(book_instance , context={'request': request})
            
            return Response(
                {
                    "details": {
                        "message": "Book got successfully",
                        "data": serializer.data 
                    }
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Error retrieving book"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteBookView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self , request, book_id):
        try:
            current_user = request.user
            book = BookModel.objects.filter(id = book_id).first()
            book_uploaded_by = book.uploaded_by
            if current_user == book_uploaded_by:
                book.delete()
                return Response(
                    {"details": "Successfully deleted"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"details": "You can not delete other person's book"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Something went wrong while deleting"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateBookView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, book_id):
        try:
            book = BookModel.objects.filter(id= book_id).first()
            current_user = request.user
            book_upload_by = book.uploaded_by
            if not book:
                return Response(
                    {"details": "Book not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = UpdateBookSerializer(instance = book , data = request.data, partial = True)
            if serializer.is_valid():
                if current_user == book_upload_by:
                    serializer.save()
                    return Response(
                        {"details": "Successfully updated book"},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {"details": "You can not update other person's book"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(
                {"details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            print("Error: ", e)
            return Response(
                {"details": "Server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )