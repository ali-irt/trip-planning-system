# estimation/management/commands/import_destinations.py
from django.core.management.base import BaseCommand
from Utrip.models import Destination as UtripDestination
from estimation.models import Destination as EstimationDestination

class Command(BaseCommand):
    help = 'Automatically saves Utrip destinations to Estimation'

    def handle(self, *args, **kwargs):
        # Fetch all destinations from Utrip app
        utrip_destinations = UtripDestination.objects.all()

        # Loop through each Utrip destination and create a corresponding Estimation destination
        for utrip_destination in utrip_destinations:
            EstimationDestination.objects.get_or_create(
                name=utrip_destination.name,
                city=utrip_destination.city  # Assuming city is a ForeignKey
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created: {utrip_destination.name}'))

        self.stdout.write(self.style.SUCCESS('All destinations have been saved.'))
