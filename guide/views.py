from django.shortcuts import render

# Create your views here.
# guide/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from .forms import UserProfileForm, TripPlanForm
from .models import Destination, TripPlan, UserProfile
from reportlab.pdfgen import canvas
from django.http import HttpResponse

# guide/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Send welcome email
            subject = 'Welcome to Travel Guide'
            message = 'Thank you for registering with Travel Guide!'
            from_email = 'travelguide689@gmail.com'
            user.email_user(subject, message, from_email)
            # Log in the user with the specified backend
            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            login(request, user)
            return redirect(reverse('home/'))
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile view after saving
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,  # Pass profile data to template
    }
    return render(request, 'profile.html', context)

def plan_trip(request):
    if request.method == 'POST':
        form = TripPlanForm(request.POST)
        if form.is_valid():
            trip_plan = form.save(commit=False)
            trip_plan.user = request.user
            trip_plan.total_price = calculate_price(trip_plan)
            trip_plan.save()
            return redirect('generate_pdf', trip_id=trip_plan.id)
    else:
        form = TripPlanForm()
    return render(request, 'plan_trip.html', {'form': form})

def calculate_price(trip_plan):
    # Logic to calculate price based on budget and transport
    return 1000  # Placeholder value

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from django.http import HttpResponse
from .models import TripPlan

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.conf import settings
from django.contrib.staticfiles import finders  # For finding static files

def generate_pdf(request, trip_id):
    trip_plan = TripPlan.objects.get(id=trip_id)

    # Create a PDF response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="trip_plan.pdf"'

    # Create a canvas
    p = canvas.Canvas(response, pagesize=letter)

    # Set up PDF styles
    p.setLineWidth(1)
    p.setTitle("Trip Plan")

    # Draw header with website name
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Travel Guide")
    p.setFont("Helvetica-Bold", 12)
    p.drawString(250, 780, "Owner: DevSquad")

    # Draw horizontal line under header
    p.line(30, 770, 570, 770)

    # Draw travel emojis or images
    emoji_path = finders.find('images/airplane.png')  # Example path to an image file
    if emoji_path:
        p.drawImage(emoji_path, 50, 760, width=40, height=40)

    # Draw trip plan details
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Trip Plan for {trip_plan.user.username}")
    p.drawString(100, 710, f"Destination: {trip_plan.destination.name}")
    p.drawString(100, 690, f"Budget: {trip_plan.get_budget_display()}")
    p.drawString(100, 670, f"Days: {trip_plan.days}")
    p.drawString(100, 650, f"Transport: {trip_plan.get_transport_display()}")
    p.drawString(100, 630, f"Total Price: ${trip_plan.total_price}")

    # Draw borders around the trip plan details section
    p.rect(90, 620, 400, 140)

    # Save the PDF
    p.showPage()
    p.save()

    return response





from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


from django.shortcuts import render, redirect
from .models import TripPlan, Destination
from .forms import TripPlanForm  # Assuming you have a form defined for TripPlan

def plan_trip(request):
    if request.method == 'POST':
        form = TripPlanForm(request.POST)
        if form.is_valid():
            destination_id = form.cleaned_data['destination']
            destination = Destination.objects.get(id=destination_id)
            days = form.cleaned_data['days']
            transport = form.cleaned_data['transport']
            total_price = form.cleaned_data['total_price']

            # Create TripPlan instance
            trip_plan = TripPlan(
                user=request.user,
                destination=destination,
                days=days,
                transport=transport,
                total_price=total_price,
            )
            trip_plan.save()  # This will trigger calculate_budget and generate_roadmap in the save method

            return redirect('trip_plan_detail', pk=trip_plan.pk)  # Redirect to trip plan detail page
    else:
        form = TripPlanForm()

    destinations = Destination.objects.all()
    context = {
        'form': form,
        'destinations': destinations,
    }
    return render(request, 'plan_trip.html', context)

