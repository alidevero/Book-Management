from django.shortcuts import get_object_or_404, render
from Auth.models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.

class LikeView(APIView):
    def post(self , request , book_id):
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                secret_key = os.environ.get('JWT_SECRET_KEY')
                payload = jwt.decode(token , secret_key , algorithms=['HS256'])
                email = payload.get('email')
                user = User.objects.filter(email=email).first()
            book = get_object_or_404(BookModel , id=book_id)
            like , created = LikeModle.objects.get_or_create(user = user ,book = book)

            if  created:
                return Response("Like successfully")
            return Response("Already Liked ")
        
        except Exception as e:

            return Response({'message':str(e),})
        


class GetAllLikeView(APIView):
    def get(self, request,book_id):
        try:
            likes_of_book = LikeModle.objects.filter(book=book_id ).all()
            serializer = GetAllLikes(likes_of_book,many=True)
            return Response(serializer.data)
        except Exception as e :
            return Response({"error" : str(e)})

#need modification for better error handling 
class CommentView(APIView):

    def post(self,request):

        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                secret_key = os.environ.get('JWT_SECRET_KEY')
                payload = jwt.decode(token , secret_key , algorithms=['HS256'])
                email = payload.get('email')
                user = User.objects.filter(email=email).first()
                
                print(f"got the user {user}")
                if not user:
                    return Response({"message":"User not found"})
                book_id = request.data.get('book_id')
                book = BookModel.objects.filter(id = book_id).first()

                print(f"got the book_id {book_id}")
                comment = request.data.get('comment')
                print(f"got the comment {comment}")
                serialzer = CommentSerializer(data ={'user':user.id,'book':book.id,'comment':comment})
                if serialzer.is_valid():
                    serialzer.save(user = user, book = book)
                    return Response({"message":"commented successfully"})
                return Response({"message":"something went wrong","error":serialzer.errors})
            return Response({"message":"Token was empty or expired"})
                
        
        except Exception as e:
            return Response({"message":str(e)})
        
    
class GetAllComments(APIView):

    def get(self ,request, book_id):
        try:            
            book_comments = CommentModel.objects.filter(book = book_id).all()
            print(f"got all comments {book_comments}")
            serializer = GetAllCommentSerializer(book_comments , many = True)
                        
            return Response(serializer.data)
                    
        except Exception as e:
            return Response({"erro":str(e)})

