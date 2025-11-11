"""
Django management command to load commentaries and cross-references from CSV into the database.
Usage: python manage.py load_commentaries
"""
import csv
import os
from django.core.management.base import BaseCommand
from bolls.models import Commentary


class Command(BaseCommand):
    help = 'Load commentaries and cross-references from CSV file into the database'

    def handle(self, *args, **options):
        # Path to the CSV file
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))),
            'commentaries',
            'commentaries.csv'
        )

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found: {csv_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Loading commentaries from: {csv_path}'))

        # Check if commentaries already exist
        existing_count = Commentary.objects.count()
        if existing_count > 0:
            self.stdout.write(self.style.WARNING(f'Database already has {existing_count} commentaries.'))
            response = input('Do you want to delete and reload? (yes/no): ')
            if response.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Aborted.'))
                return

            self.stdout.write('Deleting existing commentaries...')
            Commentary.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Deleted.'))

        # Load from CSV
        try:
            commentaries_to_create = []
            batch_size = 1000
            total_loaded = 0

            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    commentary = Commentary(
                        translation=row['translation'],
                        book=int(row['book']),
                        chapter=int(row['chapter']),
                        verse=int(row['verse']),
                        text=row['text']
                    )
                    commentaries_to_create.append(commentary)

                    # Insert in batches for better performance
                    if len(commentaries_to_create) >= batch_size:
                        Commentary.objects.bulk_create(commentaries_to_create)
                        total_loaded += len(commentaries_to_create)
                        self.stdout.write(f'Inserted {total_loaded} commentaries...')
                        commentaries_to_create = []

                # Insert remaining commentaries
                if commentaries_to_create:
                    Commentary.objects.bulk_create(commentaries_to_create)
                    total_loaded += len(commentaries_to_create)

                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {total_loaded} commentaries!'))
                self.stdout.write(self.style.SUCCESS('Cross-references are now accessible via the API.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading commentaries: {str(e)}'))
            raise
