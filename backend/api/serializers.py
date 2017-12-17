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
    id = serializers.UUIDField(read_only=True)
    image = serializers.ImageField()
    watermark_image = serializers.ImageField(read_only=True)
    user = UserSerializer(source='author', read_only=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.SerializerMethodField()
    is_hotdog = serializers.BooleanField(read_only=True)
    desc = serializers.CharField()

    class Meta:
        model = Picture
        fields = ('id', 'tags', 'created_at', 'user', 'image',
                  'watermark_image', 'author', 'is_hotdog', 'desc')
        depth = 0

    def get_tags(self, obj):
        queryset = Score.objects.filter(picture=obj).order_by('-value')
        return [ScoreSerializer(i).data for i in queryset]


class PictureSerializerUpdate(PictureSerializer):
    image = serializers.ImageField(read_only=True)
    watermark_image = serializers.ImageField(read_only=True)
