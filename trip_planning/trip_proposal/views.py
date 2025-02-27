from django.shortcuts import render, redirect
from .forms import TripProposalForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


def trip_proposal_view(request):
    if request.method == 'POST':
        form = TripProposalForm(request.POST)
        print(request.POST)  # Debugging
        if form.is_valid():
            trip_proposal = form.save(commit=False)
            trip_proposal.proposer = request.user
            trip_proposal.save()

            destination = form.cleaned_data.get('City')  # Ensure correct field name
            date = form.cleaned_data.get('date')
            email = form.cleaned_data.get('email')

            subject = 'You have got an invitation'
            destination_text = ", ".join(destination) if isinstance(destination, (list, tuple)) else destination
            message = f'Your friend {request.user.first_name} is inviting you for a trip to {destination_text} on {date}.'    
            email_from = 'travellmaatte@gmail.com'
            recipient_list = [email]

            try:
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, 'Invitation sent successfully!')
            except Exception as e:
                messages.error(request, 'There was an error sending your invitation.')
                print(f"Error sending email: {e}")

            return redirect('proposal_success')
        else:
            print(form.errors)  # Debugging: Print form validation errors
            messages.error(request, "Form submission failed. Please check your inputs.")
    else:
        form = TripProposalForm()

    return render(request, 'trip_proposal.html', {'form': form})

def proposal_success_view(request):
    return render(request, 'proposal_success.html')