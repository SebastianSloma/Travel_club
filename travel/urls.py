
from django.urls import path
from . import views

urlpatterns = [

path('', views.home, name='home'),
    path('<int:year>/<str:month>', views.home, name='home'),
    path('travels', views.all_travels, name='list-travels'),
    path('add_venue', views.add_venue, name='add-venue'),
    path('list_venues', views.list_venues, name='list-venues'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue')
]