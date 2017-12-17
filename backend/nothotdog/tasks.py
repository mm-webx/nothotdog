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
