from django.core.management.base import BaseCommand
from appfeel.models import Therapies
import csv

class Command(BaseCommand):
    help = 'Uploads a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    # Function to check if therapy exists
    @staticmethod
    def therapy_exists(description):
        return Therapies.objects.filter(description=description).exists()

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        with open(csv_file, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            # Skip the first two rows
            next(reader)
            next(reader)

            # Iterate over each row with index
            for _, row in enumerate(reader):
              
                # Access the columns
                therapy_name = row[0]
                category = row[1]
                description = row[2]
                acronyms = row[4]

                 # Check if therapy exists
                if self.therapy_exists(description):
                    print(f"Therapy '{description}' already exists. Skipping...")
                    continue

                # Create and save the new therapy
                therapy = Therapies(name=therapy_name, category=category, description=description, acronyms=acronyms)
                therapy.save()

                print(f"Saved therapy: {therapy_name}, {category}, {description}, {acronyms}")


        self.stdout.write(self.style.SUCCESS('CSV file uploaded successfully!'))
