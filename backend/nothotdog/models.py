import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from nothotdog.tasks import compute_picture, create_watermark_image
from nothotdog.utils import path_and_rename, path_and_rename_watermark


class Tag(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Picture(models.Model):
    COMPUTED_PENDING = 0
    COMPUTED_IN_PROGRESS = 1
    COMPUTED_COMPLETED = 2
    COMPUTED_ERROR = 3
    COMPUTED_FORCE = 4

    COMPUTED_STATUSES = (
        (COMPUTED_PENDING, 'pending'),
        (COMPUTED_IN_PROGRESS, 'in progress'),
        (COMPUTED_COMPLETED, 'completed'),
        (COMPUTED_ERROR, 'error'),
        (COMPUTED_FORCE, 'force')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    image = models.ImageField(upload_to=path_and_rename, null=False)
    watermark_image = models.ImageField(upload_to=path_and_rename_watermark, null=True, blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField('Tag', through='Score', through_fields=('picture', 'tag'))
    is_hotdog = models.BooleanField('Is Hot Dog?', default=False)

    computed_status = models.PositiveSmallIntegerField(choices=COMPUTED_STATUSES, null=False, default=COMPUTED_FORCE)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)

        if self.computed_status is None or self.computed_status == self.COMPUTED_FORCE:
            self.compute()

    def compute(self):
        self.computed_status = self.COMPUTED_PENDING
        self.save()
        compute_picture.delay(self.id)

    def calculate_is_hotdog(self, create_watermark_image_file=True):
        tag = settings.APP_TAG
        min_score = settings.APP_TAG_MIN_SCORE
        tag_exists = self.tags.filter(name__icontains=tag, score__value__gte=min_score).exists()

        if tag_exists:
            self.is_hotdog = True
        else:
            self.is_hotdog = False

        if create_watermark_image_file:
            self.create_image_with_watermark()

        self.save()

        return self.is_hotdog

    def add_tag(self, tag_name, score_value):
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        score, score_created = Score.objects.get_or_create(picture=self, tag=tag)
        score.value = score_value
        score.save()

        return score

    def remove_image_file(self):
        path = self.image.path
        if os.path.isfile(path):
            os.remove(path)

    def remove_watermark_image_file(self):
        if self.watermark_image:
            path = self.watermark_image.path
            if os.path.isfile(path):
                os.remove(path)

    def remove_files(self):
        self.remove_watermark_image_file()
        self.remove_image_file()

    def get_watermark_image(self):
        if not self.watermark_image:
            return self.image

    def create_image_with_watermark(self):
        create_watermark_image.delay(self.id)

    def set_watermark_image(self, file_name):
        if self.watermark_image:
            self.remove_watermark_image_file()
        image = File(open(file_name, 'rb'))
        self.watermark_image = image
        self.save()


class Score(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    value = models.FloatField('Score', default=0)

    def __str__(self):
        return '{}-{}'.format(self.picture_id, self.tag.name)

    class Meta:
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'

        unique_together = ('picture', 'tag')


@receiver(pre_delete, sender=Picture)
def save_user_profile(sender, instance, **kwargs):
    # TODO: always can be do better
    instance.remove_files()
