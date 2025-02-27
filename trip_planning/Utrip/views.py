from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from socket import timeout
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from estimation.models import *
from math import ceil 
from .forms import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from estimation.views import *

def home(request):
    dests = Destination.objects.all()[:5]
    return render(request, 'index.html', {'dests': dests})


def about(request):
    return render(request, 'about.html')


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
        else:
            user = User.objects.create_user( email=email,password=password)
            user.is_active = False  # Set user to inactive until they verify OTP
            user.save()
            send_otp(user)
            messages.success(request, 'Account created! OTP has been sent to your email for verification.')
            return redirect('verify_otp', user_id=user.id)

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Replace 'home' with the name of your home view
        else:
            # Invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def destination_list(request, destination_spot=None):
    destinations = Destination.objects.all()  # Start with all destinations
    print("Initial Destinations Count:", destinations.count())

    keyword = request.GET.get('keyword', '')
    category = request.GET.get('category', '')
    city = request.GET.get('city', '')
    spot = request.GET.get('spot', '')

    if keyword:
        destinations = destinations.filter(Q(keywords__icontains=keyword))
        print("Filtered by keyword count:", destinations.count())

    if category:
        destinations = destinations.filter(category__category_name__iexact=category)
        print("Filtered by category count:", destinations.count())

    if city:
        destinations = destinations.filter(city__name__iexact=city)
        print("Filtered by city count:", destinations.count())

    if spot:
        destinations = destinations.filter(destination_spot__icontains=spot)
        print("Filtered by spot count:", destinations.count())

    context = {
        'destinations': destinations,
        'keyword': keyword,
        'category': category,
        'city': city,
        'spot': spot,
        'categories': Category.objects.all(),
        'cities': City.objects.all(),
    }
    return render(request, 'travel_destination.html', context)


@login_required
def destination_details(request, destination_name):
    # Retrieve the destination object based on destination_name
    dest = get_object_or_404(Destination, destination_spot=destination_name)

    # Fetch accommodations related to the city from the destination
    accommodations = Accommodation.objects.filter(destination=dest.city)  # Use the related city

    # Retrieve reviews related to this destination
    reviews = ReviewRating.objects.filter(destination=dest)

    # Initialize the review form
    form = ReviewForm1()

    # Calculate number of slides for displaying reviews
    n = len(reviews)
    nSlides = ceil(n / 4)

    context = {
    'accommodations': accommodations,
    'destination': dest,
    'reviews': reviews,
    'no_of_slides': nSlides,
    'range': range(1, nSlides + 1),
    'form': form
}

    return render(request, 'destination_details.html', context)

def submit_review(request , DetailedDesc_id):
    url = request.META.get('HTTP_REFERER')  # Capture the referring URL
    if request.method == 'POST':
        form = ReviewForm1(request.POST)
        detailed_desc = get_object_or_404(Destination, id=DetailedDesc_id)  # Use get_object_or_404 for better error handling

        if form.is_valid():
            rating = form.cleaned_data['rating']
            review = form.cleaned_data['review']

            ip_address = request.META.get('REMOTE_ADDR')  # Capture the user's IP address

            # Try to get an existing review by the user for the given destination
            existing_review = ReviewRating.objects.filter(user=request.user, destination=detailed_desc).first()

            if existing_review:
                # Update the existing review
                existing_review.rating = rating
                existing_review.review = review
                existing_review.ip = ip_address
                existing_review.save()
                messages.success(request, 'Thank you! Your review has been updated.')
            else:
                # Create a new review
                new_review = ReviewRating(
                    rating=rating,
                    review=review,
                    ip=ip_address,
                    destination=detailed_desc,
                    user=request.user
                )
                
                new_review.save()
                messages.success(request, 'Thank you! Your review has been submitted.')

            return redirect(url)

    # If not a POST request or form is invalid, redirect to the referring URL
    return redirect(url)



def search(request):
    query = request.GET.get('search', '').strip()
    if not query:
        messages.warning(request, "Please enter a search term.")
        return render(request, 'search_results.html', {'allspots': [], 'query': query})

    if len(query) > 78:
        allspots = Destination.objects.none()
    else:
        alldestination = Destination.objects.filter(destination_spot=query)
        allprovince = Destination.objects.filter(province__icontains=query)
        allcity = Destination.objects.filter(CITY__icontains=query)
        allkey = Destination.objects.filter(Keywords__icontains=query)
        allspots = alldestination.union(allcity, allprovince, allkey)

    if not allspots.exists():
        messages.warning(request, "No search results found. Please refine your query.")

    params = {'allspots': allspots, 'query': query}
    return render(request, 'search_results.html', params)@login_required(login_url='login')


def send_otp(user):
    otp, created = OTP.objects.get_or_create(user=user)
    otp.generate_otp()

    # Send email
    subject = 'Your OTP for Email Verification'
    message = f'Your OTP is {otp.otp}. It is valid for 5 minutes.'
    email_from = 'travellmaatte@gmail.com'
    recipient_list = [user.email]

    send_mail(subject, message, email_from, recipient_list)


def email_verification_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            send_otp(user)
            messages.success(request, 'OTP has been sent to your email.')
            return redirect('verify_otp', user_id=user.id)
        else:
            messages.error(request, 'No user found with this email.')

    return render(request, 'email_verification.html')


def verify_otp_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    otp_instance = OTP.objects.filter(user=user).first()

    if request.method == 'POST':
        otp = request.POST.get('otp')

        if otp_instance and otp_instance.otp == otp:
            # Ensure that created_at is timezone-aware
            created_at = timezone.make_aware(otp_instance.created_at) if otp_instance.created_at.tzinfo is None else otp_instance.created_at
            time_diff = timezone.now() - created_at

            # Check if OTP is still valid (e.g., within 5 minutes)
            if time_diff <= timedelta(minutes=5):
                user.is_active = True  # Activate user upon OTP verification
                user.save()
                otp_instance.delete()  # OTP is used, so remove it
                messages.success(request, 'Your email has been verified and your account is activated.')
                return redirect('login')
            else:
                messages.error(request, 'OTP has expired.')
        else:
            messages.error(request, 'Invalid OTP.')

    return render(request, 'verify_otp.html', {'user': user})

@login_required
def profile_user(request):
    user = request.user
    try:
        profile = user.profile  # Access the related Profile object
    except Profile.DoesNotExist:
        profile = None

    join_date = user.date_joined.strftime("%B %d, %Y") if user.date_joined else "Date not available"

    return render(request, "user_profile.html", {
        "username": user.username,
        "email": user.email,
        "city": profile.city if profile else "Not specified",
        "phone": profile.phone if profile else "Not specified",
        "join_date": join_date,
    })
def faq_view(request):
    faq = Faq.objects.all()
    return render(request, 'faq.html',{'faq':faq})