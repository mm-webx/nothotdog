from django.contrib.auth.models import User
from rest_framework import viewsets

from api.serializers import PictureSerializer, UserSerializer
from nothotdog.models import Picture


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.filter(computed_status=Picture.COMPUTED_COMPLETED, watermark_image__isnull=False)
    serializer_class = PictureSerializer
    ordering = ('-created_at',)

    def get_queryset(self):
        queryset = Picture.objects.filter(computed_status=Picture.COMPUTED_COMPLETED, watermark_image__isnull=False)

        is_hotdog = self.request.query_params.get('is_hotdog', None)
        if is_hotdog is not None:
            queryset = queryset.filter(is_hotdog=is_hotdog)

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__name=tag)

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(tags__name__icontains=search)

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
