from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers

from blogs.models import Post


class BlogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ("title", "image", "subtitle", "date_public")


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('owner', 'image')


class BlogUserSerializer(serializers.ModelSerializer):

    URL = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "URL")

    def get_URL(self, obj):
        return reverse('blog_detail', args=[obj.username])
