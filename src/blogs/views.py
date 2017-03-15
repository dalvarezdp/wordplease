from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.shortcuts import render

from blogs.models import Post
# Create your views here.


def posts_list(request):
    """
    Recupera todos los post de la base de datos y las pinta
    :param request: HttpRequest
    :return: HttpResponse
    """

    # recuperar todos los post de la base de datos
    posts = Post.objects.select_related("owner").all().order_by('-date_public')

    # devolver la respuesta
    context = {
        'post_objects': posts
    }
    return render(request, 'blogs/list.html', context)


def blogs_list(request):
    """
    Recupera todos los blogs de la base de datos y los pinta
    :param request: HttpRequest
    :return: HttpResponse
    """

    # recuperar todos los post de la base de datos
    userBlogs = Post.objects.values_list('owner').distinct()

    blogs = User.objects.filter(pk=userBlogs)

    print(blogs)
    # devolver la respuesta
    context = {
        'blog_objects': blogs
    }
    return render(request, 'blogs/blogs_list.html', context)


def blog_detail(request, username):
    """
    Recupera todos los post de un usuario de la base de datos y los pinta
    :param request: HttpRequest
    :return: HttpResponse
    """

    user = User.objects.get(username=username)

    # recuperar todos los post de la base de datos
    posts = Post.objects.select_related("owner").filter(owner__username=username).order_by('-date_public')

    # devolver la respuesta
    context = {
        'user': user,
        'post_objects': posts
    }
    return render(request, 'blogs/blog_detail.html', context)