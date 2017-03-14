from django.contrib.auth.decorators import login_required
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
    # Coalesce('summary', 'headline').desc()

    # devolver la respuesta
    context = {
        'post_objects': posts
    }
    return render(request, 'blogs/list.html', context)

