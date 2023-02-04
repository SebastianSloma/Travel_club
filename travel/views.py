from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Travel, Venue

from django.contrib.auth.models import User
from .forms import VenueForm, TravelForm, TravelFormAdmin
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# import pagination stuff
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

# Show travels


def show_travel(request, travel_id):
    travel = Travel.objects.get(pk=travel_id)
    return render(request, 'travel/show_travel.html', {'travel': travel})


# Show travels in a venue
def venue_travels(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    travels = venue.travel_set.all()
    if travels:
        return render(request, 'travel/venue_travels.html', {'travels': travels})

    else:
        messages.success(request, ("That Venue Has No Events At This Time..."))
        return redirect('admin_approval')


# Create Admin Travel Approval Page
def admin_approval(request):
    venue_list = Venue.objects.all()
    travel_count = Travel.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    travel_list = Travel.objects.all().order_by('-travel_date')
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            # ucheck all travels
            travel_list.update(approved=False)
            # update database
            for x in id_list:
                Travel.objects.filter(pk=int(x)).update(approved=True)

            messages.success(
                request, ('Travel list approval has been updated!'))
            return redirect('list-travels')
        else:
            return render(request, 'travel/admin_approval.html', {
                'travel_list': travel_list,
                'travel_count': travel_count,
                'venue_count': venue_count,
                'user_count': user_count,
                'venue_list': venue_list})
    else:
        messages.success(
            request, ('You are not authorized to view this page!'))
        return redirect('home')

    return render(request, 'travel/admin_approval.html')


# Create My Travels Page
def my_travels(request):
    if request.user.is_authenticated:
        me = request.user.id
        travels = Travel.objects.filter(attendees=me)
        return render(request, 'travel/my_travels.html', {'travels': travels})

    else:
        messages.success(request, ('You are not Authorized To View This Page'))
        return redirect('home')

# Generate PDF File Venue List


def venue_pdf(request):
    # Create bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont('Helvetica', 14)

    # Designate the model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append('.')

    # loop
    for line in lines:
        textobj.textLine(line)

    # finish up
    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

# Generate CSV File Venue List


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate The Model
    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code',
                    'Phone', 'Web Address', 'Email'])

    # Loop Thu and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code,
                        venue.phone, venue.web, venue.email_address])

    return response

# Generate Text File Venue List


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []
    # Loop Thu and output
    for venue in venues:
        lines.append(
            f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')

    # Write To TextFile
    response.writelines(lines)
    return response


# Delete a Venue function

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


# Delete an travel function

def delete_travel(request, travel_id):
    travel = Travel.objects.get(pk=travel_id)
    if request.user == travel.manager:
        travel.delete()
        messages.success(request, ('Travel Deleted!'))
        return redirect('list-travels')
    else:
        messages.success(
            request, ('You Are Not Authorized To Delete This Travel!'))
        return redirect('list-travels')


def add_travel(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = TravelFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_travel?submitted=True')
        else:
            form = TravelForm(request.POST)
            if form.is_valid():
                travel = form.save(commit=False)
                travel.manager = request.user
                travel.save()
                return HttpResponseRedirect('/add_travel?submitted=True')
    else:
        # go to page, not submit
        if request.user.is_superuser:
            form = TravelFormAdmin
        else:
            form = TravelForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'travel/add_travel.html', {'form': form, 'submitted': submitted})


def update_travel(request, travel_id):
    travel = Travel.objects.get(pk=travel_id)
    if request.user.is_superuser:
        form = TravelFormAdmin(request.POST or None, instance=travel)
    else:
        form = TravelForm(request.POST or None, instance=travel)

    if form.is_valid():
        form.save()
        return redirect('list-travels')

    return render(request, 'travel/update_travel.html', {'travel': travel, 'form': form})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None,
                     request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')

    return render(request, 'travel/update_venue.html', {'venue': venue, 'form': form})


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)

        return render(request, 'travel/search_venues.html',
                      {'searched': searched, 'venues': venues})
    else:
        return render(request, 'travel/search_venues.html',
                      {})


def search_travels(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        travels = Travel.objects.filter(name__contains=searched)

        return render(request, 'travel/search_travels.html',
                      {'searched': searched, 'travels': travels})
    else:
        return render(request, 'travel/search_travels.html',
                      {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'travel/show_venue.html', {'venue': venue, 'venue_owner': venue_owner})


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('name')
    venue_list = Venue.objects.all()

    # Set up Pagination
    p = Paginator(Venue.objects.all(), 8)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = 'a' * venues.paginator.num_pages

    return render(request, 'travel/venue.html', {'venue_list': venue_list, 'venues': venues, 'nums': nums})


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    form = VenueForm
    return render(request, 'travel/add_venue.html', {'form': form, 'submitted': submitted})


def all_travels(request):
    travel_list = Travel.objects.all().order_by('-travel_date')
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

    # Query the travels model for dates
    travel_list = Travel.objects.filter(
        travel_date__year=year,
        travel_date__month=month_number

    )

    time = now.strftime('%I:%M:%S %p')
    return render(request, 'travel/home.html', {
        'name': name,
        'year': year,
        'month': month,
        'month_number': month_number,
        'cal': cal,
        'current_year': current_year,
        'time': time,
        'travel_list': travel_list,
    })
