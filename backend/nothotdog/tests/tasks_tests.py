import uuid

import pytest
from google.cloud import vision

from nothotdog.models import Picture
from nothotdog.tasks import compute_picture
from nothotdog.tests.models_tests import TestPictureFixtures
from vision.services import Label, GoogleVisionService

pytestmark = pytest.mark.django_db


class TestTask(TestPictureFixtures):
    def test_compute_task_no_picture(self):
        task = compute_picture(uuid.uuid4())
        assert task is False, 'Should task be failed'

    def test_compute_task(self, picture, monkeypatch):
        test_labels = [
            Label('label_one', 0.1),
            Label('label_two', 0.2)
        ]

        class Response(object):
            def __init__(self, labels):
                self.label_annotations = labels

        class ImageAnnotatorClient(object):
            def __init__(self):
                pass

            def label_detection(*args, **kwargs):
                return Response(test_labels)

        def prepare_image(*args, **kwargs):
            pass

        monkeypatch.setattr(vision, 'ImageAnnotatorClient', ImageAnnotatorClient)
        monkeypatch.setattr(GoogleVisionService, '_prepare_image', prepare_image)

        picture_id = picture.id
        assert not picture.tags.filter(name=test_labels[0].description, score__value=test_labels[0].score).exists()

        task = compute_picture(picture_id)
        assert task, 'Should task be done'

        get_picture = Picture.objects.get(id=picture_id)
        assert get_picture.computed_status == Picture.COMPUTED_COMPLETED
        assert get_picture.tags.filter(name=test_labels[0].description, score__value=test_labels[0].score).exists()
        assert get_picture.tags.count() == len(test_labels)

    def test_compute_task_error(self, picture, monkeypatch):
        error_msg = 'test_value_error'

        class ImageAnnotatorClient(object):
            def __init__(self):
                pass

            def label_detection(*args, **kwargs):
                raise ValueError(error_msg)

        def prepare_image(*args, **kwargs):
            pass

        monkeypatch.setattr(vision, 'ImageAnnotatorClient', ImageAnnotatorClient)
        monkeypatch.setattr(GoogleVisionService, '_prepare_image', prepare_image)

        picture_id = picture.id
        assert picture.tags.count() == 0

        compute_picture(picture_id)

        get_picture = Picture.objects.get(id=picture_id)
        assert get_picture.computed_status == Picture.COMPUTED_ERROR
        assert get_picture.tags.count() == 0
