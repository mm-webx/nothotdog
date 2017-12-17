import os

from PIL import Image

from core.celery import celery_app


@celery_app.task
def compute_picture(picture_id):
    from nothotdog.models import Picture
    from vision.services import GoogleVisionService

    try:
        picture = Picture.objects.get(id=picture_id)
    except Picture.DoesNotExist:
        return False

    picture.computed_status = Picture.COMPUTED_IN_PROGRESS
    picture.save()

    try:
        gvs = GoogleVisionService(file_name=picture.image.file.name)
        labels = gvs.label_detection()
    except Exception as e:
        # TODO: add logger
        print('Picture #{} error: {}'.format(picture_id, e))
        picture.computed_status = Picture.COMPUTED_ERROR
    else:
        for label in labels:
            picture.add_tag(label.description, label.score)

        picture.calculate_is_hotdog()
        picture.computed_status = Picture.COMPUTED_COMPLETED
    finally:
        picture.save()
        # TODO: add socket message about new status

    return True


@celery_app.task
def create_watermark_image(picture_id):
    from nothotdog.models import Picture
    from django.conf import settings

    try:
        picture = Picture.objects.get(id=picture_id)
    except Picture.DoesNotExist:
        return False

    watermark_dir = os.path.join(settings.BASE_DIR, 'nothotdog', 'statics')
    if picture.is_hotdog:
        watermark = os.path.join(watermark_dir, 'hotdog.png')
    else:
        watermark = os.path.join(watermark_dir, 'nohotdog.png')

    image = Image.open(picture.image.path)
    watermark_image = Image.open(watermark)
    x = int((image.size[0] - watermark_image.size[0]) / 2)
    y = int((image.size[1] - watermark_image.size[1]) / 2)
    image.paste(watermark_image, (x, y), watermark_image)

    ext = picture.image.path.split('.')[-1]
    tmp_file_name = '{}.{}'.format(picture.id, ext)
    tmp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', tmp_file_name)
    image.save(tmp_file_path)

    picture.set_watermark_image(tmp_file_path)

    if os.path.isfile(tmp_file_path):
        os.remove(tmp_file_path)

    return True
