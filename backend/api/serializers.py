from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from api.permissions import DenyAny
from nothotdog.models import Picture, Score, Tag


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            from django.core.files.base import ContentFile
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(min_length=5)
    last_name = serializers.CharField(min_length=5)
    username = serializers.CharField(min_length=5)
    password = serializers.CharField(min_length=8)
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()

        return user

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (DenyAny,)

        return super(self).get_permissions()


class UserSerializerPicture(UserSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ('username', 'firstName', 'lastName')


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
    image = Base64ImageField(max_length=None)
    watermark_image = serializers.ImageField(read_only=True)
    user = UserSerializerPicture(source='author', read_only=True)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.SerializerMethodField()
    is_hotdog = serializers.BooleanField(read_only=True)
    desc = serializers.CharField(required=False)
    owned = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Picture
        fields = ('id', 'tags', 'created_at', 'user', 'image',
                  'watermark_image', 'author', 'is_hotdog', 'desc', 'owned')
        depth = 0

    def get_tags(self, obj):
        queryset = Score.objects.filter(picture=obj).order_by('-value')
        return [ScoreSerializer(i).data for i in queryset]

    def get_owned(self, obj):
        if self.context['request'].user == obj.author:
            return True

        return False


class PictureSerializerUpdate(PictureSerializer):
    image = serializers.ImageField(read_only=True)
    watermark_image = serializers.ImageField(read_only=True)
