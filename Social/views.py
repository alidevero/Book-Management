from django.shortcuts import get_object_or_404, render
from Auth.models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
import os
from dotenv import load_dotenv
from Auth.authentication import *
from rest_framework import permissions , status
load_dotenv()

# Create your views here.

class LikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self , request , book_id):
        try:
            user = request.user
            book = get_object_or_404(BookModel , id=book_id)
            like , created = LikeModle.objects.get_or_create(user = user ,book = book)
            if  created:
                return Response({"message":"Liked successfully"},status=status.HTTP_200_OK)
            return Response({"message":"Already liked"})       
        except Exception as e:
            return Response({"message":"Something went wrong","error":str(e),},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UnlikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =[permissions.IsAuthenticated]
    def delete(self,request,book_id):
        try:
            user = request.user
            user_id = user.id
            like = LikeModle.objects.filter(user = user_id,book = book_id).first()
            like.delete()
            return Response({"message":"Unliked"},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"message":"Server error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllLikeView(APIView):
    def get(self, request,book_id):
        try:
            likes_of_book = LikeModle.objects.filter(book=book_id ).all()
            serializer = GetAllLikes(likes_of_book,many=True)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"message":"Something went wrong server error","error" : str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            book_id = request.data.get('book_id')
            book = BookModel.objects.filter(id = book_id).first()
            comment = request.data.get('comment')
            serialzer = CommentSerializer(data ={'user':user.id,'book':book.id,'comment':comment})
            if serialzer.is_valid():
                serialzer.save(user = user, book = book)
                return Response({"message":"commented successfully"},status=status.HTTP_200_OK)
            return Response({"message":"something went wrong","error":serialzer.errors})               
        
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class GetAllComments(APIView):

    def get(self ,request, book_id):
        try:            
            book_comments = CommentModel.objects.filter(book = book_id).all()
            serializer = GetAllCommentSerializer(book_comments , many = True)
                        
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
                    
        except Exception as e:
            return Response({"erro":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ReplyToCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        try:
            user = request.user
            book_id = request.data.get('book_id')
            comment = request.data.get('comment')
            parent = request.data.get('parent')
            book= BookModel.objects.filter(id= book_id).first()
            parent = CommentModel.objects.filter(comment_id= parent).first()
            serializer = ReplyToCommentSerializer(data = {"user":user.id,"book":book.id,"parent":parent.comment_id,"comment":comment})
            if serializer.is_valid():
                serializer.save(user=user, book=book,comment=comment)
                return Response({"message":"Replied Successfully","data":serializer.data},status=status.HTTP_200_OK)
            return Response({"error":serializer.errors})
             
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateCommentVeiw(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def patch(self , request , comment_id):
        try:
            comment = CommentModel.objects.filter(comment_id= comment_id).first()
            serializer = CommentSerializer(instance = comment , data = request.data , partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Sucessfully updated the comment"},status=status.HTTP_200_OK)
            return Response({"message":"Something went wrong while updating the comment" ,"error":serializer.errors})

        except Exception as e:
            return Response({"message":"Something went wrong on server","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def delete(self , request,comment_id):
        try:
            comment = CommentModel.objects.filter(comment_id = comment_id).first()
            comment.delete()
            return Response({"message":"Deleted comment successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"somthing went wrong on server","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
