from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter, DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from blogs.models import Post
from blogs.permissions import BlogPermission, PostPermission
from blogs.serializers import BlogListSerializer, PostSerializer


class BlogViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = BlogListSerializer
    permission_classes = (BlogPermission,)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("title", "description")
    ordering_fields = ("title", "date_public")
    filter_fields = ("title", "description")


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
            posts = Post.objects.filter(owner__username=username).order_by('-date_public')
        else:
            posts = Post.objects.filter(owner__username=username).order_by('-date_public').exclude(date_public__gte=datetime.today())

        posts = get_list_or_404(self.filter_queryset(posts))

        serializer = BlogListSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermission,)
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("title", "description")
    ordering_fields = ("title", "date_public")
    filter_fields = ("title", "description")

    def create(self, request):
        """
        Create a post
        :param request: HttpRequest
        :return: Response
        """

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """
        Returns a requested user
        :param request: HttpRequest
        :param pk: post primary key
        :return: Response
        """

        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        Updates a Post with the given data
        :param request: HttpRequest
        :param pk: Post primary key
        :return: Response
        """
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """
        Deletes a Post
        :param request: HttpRequest
        :param pk: Post primary key
        :return: Response
        """
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
