from django import forms
from multiupload.fields import MultiFileField
from .models import Blog,Comment

class BlogForm(forms.ModelForm):
    images = MultiFileField(min_num=0, max_num=10, max_file_size=1024*1024*5)  # Adjust max_num and max_file_size as needed
    videos = MultiFileField(min_num=0, max_num=10, max_file_size=1024*1024*50)  # Adjust max_num and max_file_size as needed

    class Meta:
        model = Blog
        fields = ['title', 'content', 'images', 'videos']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
