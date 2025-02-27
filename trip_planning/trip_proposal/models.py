from django.db import models
from django.contrib.auth.models import User
from Utrip.models import Destination

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('declined', 'Declined'),
    ('completed', 'Completed'),
]

class TripProposal(models.Model):

    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
    destination = models.ManyToManyField(Destination, related_name='trip_proposals')
    date = models.DateField()
    invitees = models.ManyToManyField(User, related_name='trip_invites')  # Invitees
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"Trip by {self.proposer} on {self.date}"

