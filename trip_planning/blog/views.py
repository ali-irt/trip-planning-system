from django.shortcuts import render, get_object_or_404, redirect ,HttpResponse
from django.contrib import messages
from math import ceil
from .models import Blog , Reviews
from django.core.paginator import Paginator
from .forms import *
def blog(request):
    try:
        # Fetch all blogs
        post = Blog.objects.all().order_by('-published_date')
        paginator = Paginator(post, 3)  # Show 3 posts per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'blog.html', {'page_obj':page_obj})

    except Blog.DoesNotExist:
        # Specific exception handling for missing blog entries
        messages.error(request, 'No blogs found.')
        return render(request, 'blog.html')  # Render the same page with a message

    except ValueError as e:
        # Handle specific value-related errors
        messages.error(request, 'A value error occurred: {}'.format(str(e)))
        return render(request, 'error.html')  # Render a specific error page

    except KeyError as e:
        # Handle specific key-related errors
        messages.error(request, 'A key error occurred: {}'.format(str(e)))
        return render(request, 'error.html')  # Render a specific error page

    except TypeError as e:
        # Handle specific type-related errors
        messages.error(request, 'A type error occurred: {}'.format(str(e)))
        return render(request, 'error.html')  # Render a specific error page



def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    reviews = Reviews.objects.filter(blog=blog)  # Fetch related reviews

    # Calculate the number of slides (for the carousel)
    num_of_reviews = reviews.count()
    num_of_slides = ceil(num_of_reviews / 4)  # Assuming 4 reviews per slide

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'reviews': reviews,
        'range': range(num_of_slides)  # Pass range for carousel indicators
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