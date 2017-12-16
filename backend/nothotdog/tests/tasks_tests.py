import uuid

import pytest

from nothotdog.models import Picture
from nothotdog.tasks import compute_picture
from nothotdog.tests.models_tests import TestPictureFixtures

pytestmark = pytest.mark.django_db


class TestTask(TestPictureFixtures):
    def test_compute_task_no_picture(self):
        task = compute_picture(uuid.uuid4())
        assert task is False, 'Should task be failed'

    def test_compute_task(self, picture):
        picture_id = picture.id
        assert not picture.tags.filter(name='Hot Dog', score__value=0.9).exists()

        task = compute_picture(picture_id)
        assert task, 'Should task be done'

        get_picture = Picture.objects.get(id=picture_id)
        assert get_picture.computed_status == Picture.COMPUTED_COMPLETED
        assert get_picture.tags.filter(name='Hot Dog', score__value=0.9).exists()

    def test_compute_task_error(self, picture):
        # TODO: add test for exception
        pass
