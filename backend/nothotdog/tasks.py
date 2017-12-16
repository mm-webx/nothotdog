from core.celery import celery_app


@celery_app.task
def compute_picture(picture_id):
    from nothotdog.models import Picture

    try:
        picture = Picture.objects.get(id=picture_id)
    except Picture.DoesNotExist:
        return False

    picture.computed_status = Picture.COMPUTED_IN_PROGRESS
    picture.save()

    try:
        pass
    except Exception as e:
        # TODO: add logger
        print('Picture #{} error: {}'.format(picture_id, e))
        picture.computed_status = Picture.COMPUTED_ERROR
    else:
        # TODO: add google vision support
        labels_from_google_api = ['Hot Dog']
        for label in labels_from_google_api:
            picture.add_tag(label, 0.9)

        picture.computed_status = Picture.COMPUTED_COMPLETED
    finally:
        picture.save()
        # TODO: add socket message about new status

    return True
