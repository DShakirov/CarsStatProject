from django.contrib import admin
from .models import *
class EngineAdmin(admin.ModelAdmin):

    list_display = ['type', 'slug']
    list_display_links = ['type', 'slug']
    search_fields = ['type', 'slug']


class MarkAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug']
    list_display_links = ['name', 'slug']
    search_fields = ['name', 'slug']


class GenerationAdmin(admin.ModelAdmin):

    list_display = ['name', 'year_from', 'year_to']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['name', 'year_from', 'year_to']


class CarModelAdmin(admin.ModelAdmin):

    list_display = ['mark', 'name', ]
    list_display_links = ['name', ]
    search_fields = ['name', ]
    list_filter = ['mark']


class TransmissionAdmin(admin.ModelAdmin):

    list_display = ['type', 'slug']
    list_display_links = ['type', 'slug']
    search_fields = ['type', 'slug']


class GearAdmin(admin.ModelAdmin):

    list_display = ['type', 'slug']
    list_display_links = ['type', 'slug']
    search_fields = ['type', 'slug']


class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    list_display_links = ['name']
    search_fields = ['name']

class CarAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['mark', 'car_model', 'transmission', 'engine_type', 'engine_displacement', 'year', 'price', 'created_at', 'updated_at']
    list_display_links = ['mark', 'car_model']
    search_fields = ['mark', 'car_model', 'year', 'price', 'engine_type', 'transmission']
    list_filter = ['mark', 'transmission', 'engine_type']


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['id', 'title', 'slug', 'created_at', 'get_photo', 'on_top']
    list_display_links = ['id', 'title', 'slug']
    search_fields = ['title']
    list_filter = ['created_at']
    fields = ['title', 'slug','content', 'photo', 'get_photo', 'created_at', 'on_top']
    readonly_fields = ['get_photo', 'created_at',]

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return ('Фото не установлено.')

    get_photo.short_description = 'Миниатюра'

admin.site.register(Engine, EngineAdmin)
admin.site.register(Generation, GenerationAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Gear, GearAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Transmission, TransmissionAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(News, NewsAdmin)
