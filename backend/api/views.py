from rest_framework import viewsets

from api.serializers import PictureSerializer, PictureSerializerUpdate, TagSerializer
from nothotdog.models import Picture, Tag


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.filter(computed_status=Picture.COMPUTED_COMPLETED, watermark_image__isnull=False)
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

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            serializer_class = PictureSerializerUpdate
        else:
            serializer_class = PictureSerializer

        return serializer_class


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
