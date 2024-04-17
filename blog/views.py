from django.shortcuts import render,redirect,get_object_or_404
from .forms import BlogForm,CommentForm
from .models import Blog,Comment
from django.http import JsonResponse
from django.contrib.auth.models import User
 
# Create your views here.
def home(request):
    blog = Blog.objects.all().order_by('-likes','-comments')

    context  ={"blog":blog}

    return render(request, 'blog/home.html', context)




def toggle_like(request, pk):
    blog_post = get_object_or_404(Blog, pk=pk)
    user = request.user

    if user.is_authenticated:
        if user in blog_post.likes.all():
            blog_post.likes.remove(user)
            liked = False
        else:
            blog_post.likes.add(user)
            liked = True

        return JsonResponse({'liked': liked, 'like_count': blog_post.likes.count()})
    else:
        return JsonResponse({'error': 'User is not authenticated'})




def comment(request,author, pk):
    # Retrieve the blog post
    blog_post = get_object_or_404(Blog, pk=pk)

    # Retrieve all comments associated with the blog post
    comments = Comment.objects.filter(blog=blog_post)

    # Check if the request is a POST request
    if request.method == 'POST':
        # Create a comment form instance with the posted data
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # Save the comment without committing to the database
            comment = comment_form.save(commit=False)
            # Assign the blog post to the comment
            comment.blog = blog_post
            # Assign the commenter to the comment
            comment.commenter = request.user  # Assuming users are logged in
            # Save the comment to the database
            if blog_post.comment_turn == 'False':
                return JsonResponse({'403 Error': 'comment has been turned off for  this post'})
            else:
                comment.save()
    else:
        # If it's not a POST request, create an empty comment form
        comment_form = CommentForm()

    # Pass the blog post, comments, and comment form to the template
    context = {
        'blog_post': blog_post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/fullpost.html', context)










def create_post(request):
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, request.FILES)
        comment_form = CommentForm(request.POST)
        if blog_form.is_valid() and comment_form.is_valid():
            # Save the blog post
            blog_instance = blog_form.save(commit=False)
            blog_instance.author = request.user  # Set the author to the current user
            blog_instance.comment_turn = True # Set the comment turn to True or off for testing
            blog_instance.save()

            # Save the comment
            comment_instance = comment_form.save(commit=False)
            comment_instance.blog = blog_instance
            comment_instance.commenter = request.user 

        
            comment_instance.save()
            return redirect('home')  # Redirect to home page after successful post
    else:
        blog_form = BlogForm()
        comment_form = CommentForm()
    context = {'blog_form': blog_form, 'comment_form': comment_form}
    return render(request, 'blog/create.html', context)



def turn_comment(request, pk, value):
   
    blog_post = get_object_or_404(Blog, pk=pk)
    
    blog_post.comment_turn = value
    blog_post.save()
    return JsonResponse({'success': True})
     


def delete_comment(request, pk,ps ):
    blog_post = get_object_or_404(Blog, pk=ps)

    # Retrieve all comments associated with the blog post
    comment = get_object_or_404(Comment, pk=pk)

    if request.user == blog_post.author or request.user == comment.commenter:
        comment.delete()
        return JsonResponse({'success':'you deleted the comment'})
    else:
        return JsonResponse({'403':"you cannot delete this comment because you're not the author or the post owner"})
     



def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    print(pk,user)
    context = {'user': user}
    return render(request,'blog/profile.html', context)



def delete_post(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # Retrieve all comments associated with the blog post

    comments = Comment.objects.filter(blog=blog)

    if request.user == blog.author: 
        comments.delete()
        blog.delete()
        return JsonResponse({'success':'you deleted the Post'})
    else:
        return JsonResponse({'403':"you cannot delete this Post because you're not the author or the post owner"})



 