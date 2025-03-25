from django.db import models
from Books.models import BookModel
from Auth.models import User

# Create your models here.

class LikeModel(models.Model):

    like_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user' , 'book')
    def __str__(self):
        return self.like_id

class CommentModel(models.Model):

    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE)
    comment= models.TextField(max_length=500 , default= None)
    commented_at =models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE,related_name='replies')

    class Meta:
        ordering = ['commented_at']


