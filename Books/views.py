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
load_dotenv()

class UploadBookView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:    
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                secret_key = os.environ.get('JWT_SECRET_KEY')
                print("trying")
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                email = payload.get('email')
                user = User.objects.filter(email=email).first()

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
