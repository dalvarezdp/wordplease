from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter, DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blogs.models import Post
from blogs.serializers import PostsListSerializer, PostSerializer


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("title", "description")
    ordering_fields = ("title", "date_public")
    filter_fields = ("title", "description")

    def get_serializer_class(self):
        return PostsListSerializer if self.action == "list" else PostSerializer


    def list(self, request, username):
        """
        Returns el blog indicado por el username
        :param request: HttpRequest
        :return: Response
        """
        '''queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)'''

        userUrl = get_object_or_404(User, username=username)
        user = request.user

        if request.user.is_superuser or user == userUrl:
            posts = get_list_or_404(self.filter_queryset(Post.objects.filter(owner__username=username).order_by('-date_public')))
        else:
            posts = get_list_or_404(self.filter_queryset(Post.objects.filter(owner__username=username).order_by('-date_public').exclude(date_public__gte=datetime.today())))

        serializer = PostsListSerializer(posts, many=True)
        return Response(serializer.data)
