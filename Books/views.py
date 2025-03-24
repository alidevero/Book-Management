from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import BookModel
from .serializers import *
from dotenv import load_dotenv
import os 
import jwt
from Auth.models import *
from rest_framework import status, permissions
from Auth.authentication import *
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
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message":"Something went wrong in upload book view",
                "error" : str(e)
            })
    


class RetriveAllBooksView(APIView):

    def get(self , request):
        try:  
            books = BookModel.objects.all()
            serializer = ViewAllBooks(books, many = True)
            return Response(serializer.data)
        
        except Exception as e :
            return Response({
                "message": "Error while getting books",
                "error" : str(e)
            })

class RetriveSingleBookView(APIView):
    def get(self , request, book_id):
        try:
            book_instance = get_object_or_404(BookModel, id = book_id)
            serializer = ViewSingleBookSerializer(book_instance , context={'request': request})
            
            return Response({
                    "message":"Book got successfully",
                    "data": serializer.data 
                })
            
        except Exception as e:
            return Response({"error":str(e)})

class DeleteBookView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def delete(self , request,book_id):
        try:
            current_user = request.user
            book = BookModel.objects.filter(id = book_id).first()
            book_uploaded_by = book.uploaded_by
            if current_user == book_uploaded_by:
                book.delete()
                return Response({"message":"Successfully deleted"})
            return Response({"message":"You can not delete other person' book"},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message":"Something went wrong in while deleting","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateBookView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request,book_id):
        try:
            book = BookModel.objects.filter(id= book_id).first()
            current_user = request.user
            book_upload_by = book.uploaded_by
            if not book:
                return Response({"message":"book not found"},status=status.HTTP_404_NOT_FOUND)
            serializer = UpdateBookSerializer(instance = book , data = request.data, partial = True)
            if serializer.is_valid():
                if current_user == book_upload_by:
                    serializer.save()
                    return Response({"message":"Successfully updated book"},status=status.HTTP_200_OK)
                return Response({"message":"You can not update other peron's book"},status=status.HTTP_401_UNAUTHORIZED)
            return Response({"message":"Something went wrong while updating","error":serializer.errors},)
            
        except Exception as e:
            return Response({"message":"server error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

