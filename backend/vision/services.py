import io

from google.cloud import vision
from google.cloud.vision_v1 import types


class GoogleVisionService:

    def __init__(self, file_name=None):
        self._client = vision.ImageAnnotatorClient()
        self.file_name = file_name

    def _prepare_image(self):
        with io.open(self.file_name, 'rb') as image_file:
            content = image_file.read()

        return types.Image(content=content)

    def label_detection(self):
        image = self._prepare_image()
        response = self._client.label_detection(image=image)
        labels = response.label_annotations

        return labels
