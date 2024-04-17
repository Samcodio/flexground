from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    comment_turn = models.CharField(max_length=10)
    
    

    def __str__(self):
        return self.title





class BlogMedia(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='media')
    media_file = models.FileField(upload_to='blog_media/', blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    uploaded_at = models.DateTimeField(auto_now_add=True)




class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.blog.title}"

class Share(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='shares')
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
