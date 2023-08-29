# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Post


def home(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'blog/home.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})