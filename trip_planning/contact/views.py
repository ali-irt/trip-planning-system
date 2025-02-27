from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail

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
