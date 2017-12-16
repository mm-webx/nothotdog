import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)


class Picture(models.Model):
    COMPUTED_PENDING = 0
    COMPUTED_IN_PROGRESS = 1
    COMPUTED_COMPLETED = 2
    COMPUTED_ERROR = 3

    COMPUTED_STATUSES = (
        (COMPUTED_PENDING, 'pending'),
        (COMPUTED_IN_PROGRESS, 'in progress'),
        (COMPUTED_COMPLETED, 'completed'),
        (COMPUTED_COMPLETED, 'error'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    image = models.ImageField(upload_to='uploads/%Y-%m-%d/')
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField('Tag', through='Score', through_fields=('picture', 'tag'))
    is_hotdog = models.BooleanField(default=False)

    computed_status = models.PositiveSmallIntegerField(choices=COMPUTED_STATUSES, null=True, default=None)

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)

        if self.computed_status is None:
            self.compute()

    def compute(self):
        self.computed_status = self.COMPUTED_PENDING
        self.save()
        # TODO: start task

    def calculate_is_hotdog(self):
        tag = settings.APP_TAG
        min_score = settings.APP_TAG_MIN_SCORE
        tag_exists = self.tags.filter(name__icontains=tag, score__value__gte=min_score).exists()

        if tag_exists:
            self.is_hotdog = True
        else:
            self.is_hotdog = False

        self.save()

        return self.is_hotdog

    def add_tag(self, tag_name, score_value):
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        score, score_created = Score.objects.get_or_create(picture=self, tag=tag)
        score.value = score_value
        score.save()

        return score


class Score(models.Model):
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    value = models.FloatField(default=0)

    class Meta:
        unique_together = ('picture', 'tag')
