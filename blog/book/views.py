from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from .permissions import IsOwner
from .serializers import PostSerializer
from .models import Post


class PostAPIView(ListCreateAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes =(permissions.IsAuthenticated,IsOwner)

    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class PostdetailAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)