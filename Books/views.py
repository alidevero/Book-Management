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
            book = BookModel.objects.filter(id = book_id).first()
            book.delete()
            return Response({"message":"Successfully deleted"})
        except Exception as e:
            return Response({"message":"Something went wrong in while deleting","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                     