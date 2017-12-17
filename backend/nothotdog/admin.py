from django.contrib import admin
from imagekit.admin import AdminThumbnail

from nothotdog.models import Picture, Tag, Score


def run_compute(modeladmin, request, queryset):
    for item in queryset.all():
        item.computed_status = Picture.COMPUTED_FORCE
        item.save()


class ScoresInline(admin.TabularInline):
    model = Picture.tags.through


@admin.register(Picture)
class PicturesAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_hotdog', 'computed_status')
    inlines = (ScoresInline,)
    readonly_fields = ('is_hotdog', 'image_display', 'watermark_image_display', 'watermark_image', 'computed_status')
    search_fields = ('tags__name',)
    actions = [run_compute]

    image_display = AdminThumbnail(image_field='image')
    image_display.short_description = 'Image'

    watermark_image_display = AdminThumbnail(image_field='watermark_image')
    watermark_image_display.short_description = 'Image watermark'

    run_compute.short_description = 'Force run compute on selected pictures'


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Score)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'picture_id', 'tag', 'value')
    search_fields = ('tag__name',)
    readonly_fields = ('picture', 'tag')
