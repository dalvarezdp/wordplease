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


