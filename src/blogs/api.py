from rest_framework.filters import SearchFilter, OrderingFilter, DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from blogs.models import Post
from blogs.serializers import PostsListSerializer, PostSerializer


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    #permission_classes = (IsAuthenticated,)
    #filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    #search_fields = ("name", "description")
    #ordering_fields = ("id", "name", "owner", "assignee", "status", "created_at")
    #filter_fields = ("status", "owner", "assignee", "created_at", "deadline")

    def get_serializer_class(self):
        return PostsListSerializer if self.action == "list" else PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
