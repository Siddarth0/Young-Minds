from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .models import Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'create_post.html', {'form': form})

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.likes += 1
    post.save()
    return redirect('post_list')

def edit_post(request, post_id):
    post = get_object_or_404(Post, id= post_id)
    form = PostForm(request.POST, instance = post)
    if form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'edit_post.html', {'form':form, 'post':post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete_post.html', {'post':post})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


# Create your views here.
