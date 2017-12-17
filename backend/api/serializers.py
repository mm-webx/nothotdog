from django.contrib.auth.models import User
from rest_framework import serializers

from nothotdog.models import Picture, Score, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ScoreSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='tag.name')

    class Meta:
        model = Score
        fields = ('name', 'value')


class PictureSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    watermark_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Picture
        fields = ('id', 'author', 'image_url', 'watermark_image_url', 'tags', 'created_at')
        depth = 1

    def get_image_url(self, picture):
        request = self.context.get('request')
        image_url = picture.image.url
        return request.build_absolute_uri(image_url)

    def get_watermark_image_url(self, picture):
        request = self.context.get('request')
        image_url = picture.get_watermark_image().url
        return request.build_absolute_uri(image_url)

    def get_tags(self, obj):
        queryset = Score.objects.filter(picture=obj).order_by('-value')
        return [ScoreSerializer(i).data for i in queryset]
