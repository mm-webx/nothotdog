import os

from django.conf import settings
from google.cloud import vision

from vision.services import GoogleVisionService, Label


class TestLabel:
    def test_label(self):
        desc = 'test_desc'
        score = 0.8777383
        label = Label(desc, score)

        assert label.description == desc
        assert label.score == score

        assert str(label) == '{}, {}'.format(desc, score)


class TestService:
    def test_prepare_image(self, monkeypatch):
        class ImageAnnotatorClient(object):
            def __init__(self):
                pass

            def label_detection(*args, **kwargs):
                pass

        monkeypatch.setattr(vision, 'ImageAnnotatorClient', ImageAnnotatorClient)

        gvs = GoogleVisionService()
        gvs.file_name = os.path.join(settings.BASE_DIR, 'nothotdog', 'tests', 'tests_resources', 'example.jpeg')
        image = gvs._prepare_image()

        assert image.content

    def test_google_vision_service(self, monkeypatch):
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

        gvs = GoogleVisionService()
        labels = gvs.label_detection()
        assert labels[0].description == test_labels[0].description
        assert labels[0].score == test_labels[0].score
        assert labels[1].description == test_labels[1].description
        assert labels[1].score == test_labels[1].score
