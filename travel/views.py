from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Travel
from .forms import VenueForm
from django.http import HttpResponseRedirect

# Create your views here.


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form=VenueForm
        if 'submitted' in request.GET:
            submitted = True

    form = VenueForm
    return render(request, 'travel/add_venue.html', {'form':form, 'submitted':submitted})


def all_travels(request):
    travel_list = Travel.objects.all()
    return render(request, 'travel/travel_list.html', {
        'travel_list': travel_list
    })


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = 'John'
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(
        year,
        month_number
    )
    now = datetime.now()
    current_year = now.year

    time = now.strftime('%I:%M:%S %p')
    return render(request, 'travel/home.html', {
        'name': name,
        'year': year,
        'month': month,
        'month_number': month_number,
        'cal': cal,
        'current_year': current_year,
        'time': time,
    })
