from rest_framework import serializers
from .models import *

from django.shortcuts import get_object_or_404

class UploadBookSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = BookModel
        fields = ['title','author','description','pdf_content' ,'uploaded_by']

    # title = serializers.CharField()
    # author = serializers.CharField()
    # description = serializers.CharField()
    # pdf_content = serializers.FileField()

    def validate_title(self , value):
        if not value:
            raise serializers.ValidationError("Title is required")
        return value
    
    def validate_author(self,value):
        if not value:
            raise serializers.ValidationError("Author is required")
        return value
    
    def validate_pdf_content(self, value):
        if not value:
            raise serializers.ValidationError("Book PDF is required")
        return value
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    
            
class ViewAllBooks(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    description = serializers.CharField()
    pdf_content = serializers.FileField()



class ViewSingleBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(write_only=True)
    title = serializers.CharField()
    author = serializers.CharField()
    description = serializers.CharField()
    pdf_content = serializers.SerializerMethodField()


    def get_pdf_content(self, instance):
        request = self.context.get('request')
        if instance.pdf_content:
            return request.build_absolute_uri(instance.pdf_content.url)
        return None

    def to_representation(self , instance):
        return {
            "book_id":instance.id,
            "title":instance.title,
            "author":instance.author,
            "description":instance.description,
            "pdf_content":self.get_pdf_content(instance),

        }


    

    