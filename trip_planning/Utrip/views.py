from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from math import ceil
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
import logging
from django.conf import settings
from urllib.parse import quote
from django.core.paginator import Paginator


logger = logging.getLogger(__name__)


def home(request):
    dests = Destination.objects.all()[:5]
    return render(request, 'index.html', {'dests': dests})


def about(request):
    return render(request, 'about.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.is_active = False
            user.save()
            send_otp(user)
            messages.success(request, 'Account created! OTP sent to your email.')
            return redirect('verify_otp', user_id=user.id)
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


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
    form = ReviewForm()

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
        form = ReviewForm(request.POST)
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

from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from .models import Destination, City, Accommodation, Transportation, Blog

def search(request):
    query = request.GET.get('search', '').strip()
    if not query:
        messages.warning(request, "Please enter a search term.")
        return render(request, 'search_results.html', {'results': [], 'query': query})

    if len(query) > 78:
        results = []
    else:
        destination_results = Destination.objects.filter(
            Q(destination_spot__icontains=query) |
            Q(keywords__icontains=query) |
            Q(description__icontains=query) |
            Q(city__name__icontains=query) |
            Q(city__province__icontains=query) |
            Q(category__category_name__icontains=query)
        ).distinct()

        accommodation_results = Accommodation.objects.filter(
            Q(name__icontains=query) |
            Q(owner__icontains=query) |
            Q(destination__name__icontains=query) |
            Q(type__type__icontains=query) |
            Q(address__icontains=query)
        ).distinct()

        transportation_results = Transportation.objects.filter(
            Q(origin__name__icontains=query) |
            Q(origin__province__icontains=query) |
            Q(registeration_number__icontains=query) |
            Q(type__icontains=query)
        ).distinct()

        blog_results = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(blog__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()

        # Combine all results in a dictionary
        results = {
            'destinations': destination_results,
            'accommodations': accommodation_results,
            'transportation': transportation_results,
            'blogs': blog_results,
        }

    if not any(len(qs) > 0 for qs in results.values()):
        messages.warning(request, "No search results found. Please refine your query.")

    return render(request, 'search_results.html', {'results': results, 'query': query})

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

@login_required
def edit_profile(request):
    # Create Profile if not exists
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    user_form = EditUserForm(instance=request.user)
    profile_form = EditProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_user')  # Change to your desired success redirect

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# Set up logging

@login_required
def trip_proposal_view(request):
    if request.method == 'POST':
        form = TripProposalForm(request.POST)
        if form.is_valid():
            trip_proposal = form.save(commit=False)
            trip_proposal.proposer = request.user
            trip_proposal.save()

            city = form.cleaned_data.get('city')
            destination = form.cleaned_data.get('destination')
            date = form.cleaned_data.get('date')
            phone_number = form.cleaned_data.get('phone_number')

            # Ensure phone_number is provided
            if not phone_number:
                messages.error(request, "Please provide a phone number.")
                return render(request, 'trip_proposal.html', {'form': form})

            # Generate WhatsApp link
            whatsapp_link = generate_whatsapp_link(request.user, city, destination, date, phone_number)
            return redirect(whatsapp_link)
        else:
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, "Form submission failed. Please check your inputs.")
    else:
        form = TripProposalForm()

    return render(request, 'trip_proposal.html', {'form': form})



def proposal_success_view(request):
    return render(request, 'proposal_success.html')




def generate_whatsapp_link(user_name, city, destination, date, phone_number):

    location = []
    if city:
        location.append(f"city of {city.name}")  # Assuming city has a 'name' field
    if destination:
        location.append(f"{destination.destination_spot}")  # Correct field
    location_text = " and ".join(location) if location else "an unspecified location"

    # Format the message
    message = f"Your friend {user_name} is inviting you for a trip to {location_text} on {date}."

    # URL-encode the message
    encoded_message = quote(message)

    # Generate the WhatsApp link
    whatsapp_link = f"https://wa.me/{phone_number}?text={encoded_message}"
    logger.info(f"WhatsApp link generated: {whatsapp_link}")
    return whatsapp_link

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Example: Send an email with the form data
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=message,
                from_email=email,
                recipient_list=['ali233khalid@gmail.com'],
                fail_silently=False,
            )

            return HttpResponse("Thank you for your message. We will get back to you shortly.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})



def estimate_price(request):
    if request.method == 'POST':
        form = EstimationForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            destination = form.cleaned_data['destination']
            accommodation_type = form.cleaned_data['accommodation_type']
            transportation_type = form.cleaned_data['transportation_type']
            num_nights = form.cleaned_data['num_nights']
            num_people = form.cleaned_data['num_people']

            # Calculate accommodation cost
            accommodation = Accommodation.objects.filter(destination=destination, type=accommodation_type).first()
            accommodation_cost = accommodation.average_price * num_nights * num_people if accommodation else 0

            # Calculate transportation cost
            transportation = Transportation.objects.filter(destination=destination, type=transportation_type).first()
            transportation_cost = transportation.average_price if transportation else 0

            # Calculate total price
            total_price = accommodation_cost + transportation_cost

            return render(request, 'result.html', {'total_price': total_price})
    else:
        form = EstimationForm()
    return render(request, 'estimate.html', {'form': form})



@login_required
def hotel_view(request):
    if request.method == 'POST':
        form = hotelform(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            messages.success(request, 'Hotel details saved successfully!')
            return redirect('hotels')
        else:
            messages.error(request, 'There was an error saving the hotel details. Please check the form.')
    else:
        form = hotelform()

    return render(request, 'hotels.html', {'form': form})

def trans(request):
    if request.method == 'POST':
        form = TransportationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            messages.success(request, 'Transportation details saved successfully!')
            return redirect('trans')  # Redirect to a success page or any other view
        else:
            messages.error(request, 'There was an error saving the transportation details.')
    else:
        form = TransportationForm()

    return render(request, 'vehicle.html', {'form': form})

def hotel_list(request):
    hotels = Accommodation.objects.filter(is_approved=True)
    context = {
        'hotels': hotels
    }
    return render(request, 'hotel_list.html', context=context)


def hotel_details(request, hotelid):
    hotel = get_object_or_404(Accommodation,id=hotelid)
    context = {
        'hotel': hotel
        }
    return render(request, 'hotel_details.html', context=context)


def blog(request):
    try:
        # Fetch all blogs
        posts = Blog.objects.all().order_by('-published_date')
        paginator = Paginator(posts, 3)  # Show 3 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog.html', {'page_obj': page_obj, 'MEDIA_URL': settings.MEDIA_URL})

    except Blog.DoesNotExist:
        messages.error(request, 'No blogs found.')
        return render(request, 'blog.html')

    except (ValueError, KeyError, TypeError) as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return render(request, 'error.html')



def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    reviews = Reviews.objects.filter(blog=blog)

    num_of_reviews = reviews.count()
    num_of_slides = ceil(num_of_reviews / 4)

    print(f"Total Reviews: {num_of_reviews}, Slides: {num_of_slides}")

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'reviews': reviews,
        'slide_range': range(num_of_slides) if num_of_slides > 0 else range(1)  # Ensure at least one slide
    })


def submit_review_blog(request, id):
    detailed_blog = get_object_or_404(Blog, id=id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            rating = form.cleaned_data['rating']
            review_text = form.cleaned_data['review']
            ip_address = request.META.get('REMOTE_ADDR')  # Get user IP

            # Check if the user has already submitted a review
            existing_review = Reviews.objects.filter(user=request.user, blog=detailed_blog).first()

            if existing_review:
                # Update existing review
                existing_review.rating = rating
                existing_review.review = review_text
                existing_review.ip = ip_address
                existing_review.save()
                messages.success(request, 'Thank you! Your review has been updated.')
            else:
                # Create a new review
                new_review = Reviews(
                    rating=rating,
                    review=review_text,
                    ip=ip_address,
                    blog=detailed_blog,
                    user=request.user
                )
                new_review.save()
                messages.success(request, 'Thank you! Your review has been submitted.')

            return redirect('blog_detail', id=detailed_blog.id)  # Redirect to blog detail

    else:
        form = ReviewForm()

    return render(request, 'blog_detail.html', {'form': form, 'blog': detailed_blog})