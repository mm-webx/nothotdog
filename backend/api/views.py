from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from api.permissions import IsOwnerOrReadOnly
from api.serializers import PictureSerializer, PictureSerializerUpdate, TagSerializer, UserSerializer, \
    UserSerializerPicture
from nothotdog.models import Picture, Tag


class PictureViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Picture.objects.filter(watermark_image__isnull=False).order_by('-created_at')

    def get_queryset(self):
        queryset = Picture.objects.filter(watermark_image__isnull=False)

        is_hotdog = self.request.query_params.get('is_hotdog', None)
        if is_hotdog is not None:
            queryset = queryset.filter(is_hotdog=is_hotdog)

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__name=tag)

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(tags__name__icontains=search)

        queryset = queryset.order_by('-created_at').prefetch_related('author', 'score_set', 'tags')

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            serializer_class = PictureSerializerUpdate
        else:
            serializer_class = PictureSerializer

        return serializer_class


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permissions = [permissions.IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    permissions = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = UserSerializerPicture
        else:
            serializer_class = UserSerializer

        return serializer_class
