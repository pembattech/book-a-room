from django.contrib import admin
import admin_thumbnails

from .models import Hotel, HotelImage

@admin_thumbnails.thumbnail('hotel_images')
class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class HotelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [HotelImageInline]

# Register your models here.
admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelImage)