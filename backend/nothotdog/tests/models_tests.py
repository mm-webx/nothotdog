import os

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.db import IntegrityError

from nothotdog.models import Tag, Picture, Score
from nothotdog.tasks import create_watermark_image

pytestmark = pytest.mark.django_db


class TestTags:
    def test_name(self):
        test_tag = 'Hot dog'
        tag = Tag(name=test_tag)
        tag.save()

        get_tag = Tag.objects.get(id=tag.id)
        assert get_tag.name == test_tag

    def test_unique_name(self):
        test_tag = 'Hot dog unique'
        tag = Tag(name=test_tag)
        tag.save()

        error = None
        second_tag = Tag(name=test_tag)
        try:
            second_tag.save()
        except IntegrityError:
            error = True

        assert error is True, 'Should return Integrity Error'


class TestPictureFixtures:
    @pytest.fixture
    def picture(self):
        user = User.objects.create_user('test_user')
        test_file = os.path.join(settings.BASE_DIR, 'nothotdog', 'tests', 'tests_resources', 'example.jpeg')
        image = File(open(test_file, 'rb'))
        picture = Picture(image=image, author=user)
        picture.save()
        yield picture
        picture.remove_image_file()


class TestPicture(TestPictureFixtures):
    def test_picture(self, picture):
        assert picture.id is not None

    def test_remove_image_file(self, picture):
        path = picture.image.path
        assert os.path.isfile(path)
        picture.remove_image_file()
        assert not os.path.isfile(path)

    def test_add_tag(self, picture):
        tag_name = 'Hot Dog'
        score_value = 0.34
        picture.add_tag(tag_name, score_value)

        assert picture.tags.filter(name=tag_name, score__value=score_value).exists()

    def test_calculate_is_hotdog(self, picture):
        tag_name = 'Dog Food'
        score_value = 0.95
        settings.APP_TAG = tag_name
        settings.APP_TAG_MIN_SCORE = score_value

        picture.add_tag(tag_name, score_value)

        assert picture.calculate_is_hotdog(), 'Should calculate that is hotdog'

        get_picture = Picture.objects.get(id=picture.id)
        assert get_picture.is_hotdog is True

        picture.add_tag(tag_name, 0.3)

        assert not picture.calculate_is_hotdog(), 'Should calculate that is not hotdog'
        get_picture = Picture.objects.get(id=picture.id)
        assert get_picture.is_hotdog is False

        assert get_picture.tags.count() == 1

        Score.objects.filter(picture=picture).delete()

        assert not picture.calculate_is_hotdog(), 'Should calculate that is not hotdog'
        get_picture = Picture.objects.get(id=picture.id)
        assert get_picture.is_hotdog is False

        assert get_picture.tags.count() == 0

    def test_save_change_status(self, monkeypatch):
        def compute_picture(*args, **kwargs):
            pass

        from nothotdog import tasks
        monkeypatch.setattr(tasks, 'compute_picture', compute_picture)

        user = User.objects.create_user('test_user')
        test_file = os.path.join(settings.BASE_DIR, 'nothotdog', 'tests', 'tests_resources', 'example.jpeg')
        image = File(open(test_file, 'rb'))
        picture = Picture(image=image, author=user)

        assert picture.computed_status is Picture.COMPUTED_FORCE
        picture.save()
        # also test compute()
        assert picture.computed_status is Picture.COMPUTED_PENDING

        picture.remove_image_file()

    def test_remove_files(self, picture):
        picture_id = picture.id
        create_watermark_image(picture_id)

        get_picture = Picture.objects.get(id=picture_id)

        assert get_picture.watermark_image

        image = get_picture.image.path
        watermark_image = get_picture.watermark_image.path

        assert os.path.isfile(image)
        assert os.path.isfile(watermark_image)

        get_picture.remove_files()

        assert not os.path.isfile(image)
        assert not os.path.isfile(watermark_image)

    def test_get_watermark_image(self, picture):
        assert picture.image
        assert not picture.watermark_image

        assert picture.get_watermark_image() == picture.image

    def test_set_watermark_image(self, picture):
        assert picture.image
        assert not picture.watermark_image

        picture_id = picture.id
        create_watermark_image(picture_id)

        get_picture = Picture.objects.get(id=picture_id)

        assert get_picture.watermark_image
        create_watermark_image(picture_id)
