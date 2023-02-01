from django.contrib import admin
from .models import Venue
from .models import TravelUser
from .models import Travel

# Register your models here.

# admin.site.register(Venue)
admin.site.register(TravelUser)
# admin.site.register(Travel)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')


@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'travel_date', 'description', 'manager')
    list_display = ('name', 'travel_date', 'venue')
    list_filter = ('travel_date', 'venue')
    ordering = ('travel_date',)
