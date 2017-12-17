from django.contrib import admin
from imagekit.admin import AdminThumbnail

from nothotdog.models import Picture, Tag, Score


def run_compute(modeladmin, request, queryset):
    for item in queryset.all():
        item.computed_status = Picture.COMPUTED_FORCE
        item.save()


run_compute.short_description = 'Force run compute on selected pictures'


class ScoresInline(admin.TabularInline):
    model = Picture.tags.through


@admin.register(Picture)
class PicturesAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_hotdog', 'computed_status')
    inlines = (ScoresInline,)
    readonly_fields = ('is_hotdog', 'image_display')
    actions = [run_compute]

    image_display = AdminThumbnail(image_field='image')
    image_display.short_description = 'Image preview'


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Score)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'picture_id', 'tag', 'value')
