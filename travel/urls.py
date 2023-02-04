
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('<int:year>/<str:month>', views.home, name='home'),
    path('travels', views.all_travels, name='list-travels'),
    path('add_venue', views.add_venue, name='add-venue'),
    path('list_venues', views.list_venues, name='list-venues'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    path('search_venues', views.search_venues, name='search-venues'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('add_travel', views.add_travel, name='add-travel'),
    path('update_travel/<travel_id>', views.update_travel, name='update-travel'),
    path('delete_travel/<travel_id>', views.delete_travel, name='delete-travel'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('venue_text', views.venue_text, name='venue_text'),
    path('venue_csv', views.venue_csv, name='venue_csv'),
    path('venue_pdf', views.venue_pdf, name='venue_pdf'),
    path('my_travels', views.my_travels, name='my_travels'),
    path('search_travels', views.search_travels, name='search_travels'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
    path('venue_travels/<venue_id>', views.venue_travels, name='venue-travels'),
    path('show_travel/<travel_id>', views.show_travel, name='show-travel'),
]
