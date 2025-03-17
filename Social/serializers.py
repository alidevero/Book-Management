from rest_framework import serializers
from .models import *


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeModle
        fields =['like_id' , 'user' , 'book' , 'liked_at']
        read_only_fields = ['user']


    def validate_book(self , value):
        if not value:
            raise serializers.ValidationError("Book not found")
        return value
        
    def validate_user(self, value):
        if not value:
            raise serializers.ValidationError("User not found")
        return value
    
    def create(self, validated_data):
        return super().create(validated_data)
    

class GetAllLikes(serializers.Serializer):
        like_id = serializers.IntegerField()
        user = serializers.CharField()
        book = serializers.CharField()
        
    
    
class CommentSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = CommentModel
          fields = ['user' , 'book' , 'comment']

     def validate_book(self ,value):
          if not value:
               raise serializers.ValidationError("Book_id is required")
          return value
          
     def validate_comment(self,value):
          if not value:
               raise serializers.ValidationError("comment is required")
          return value
     

class GetAllCommentSerializer(serializers.Serializer):
    book = serializers.CharField()
    user = serializers.CharField()
    comment = serializers.CharField()



class ReplyToCommentSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = CommentModel
          fields = ['comment','book','parent','user']
