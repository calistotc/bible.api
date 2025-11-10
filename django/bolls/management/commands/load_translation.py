"""
Django management command to load Bible translations from ZIP files into the database.
Usage: python manage.py load_translation YLT
"""
import json
import zipfile
import os
from django.core.management.base import BaseCommand
from bolls.models import Verses


class Command(BaseCommand):
    help = 'Load a Bible translation from ZIP file into the database'

    def add_arguments(self, parser):
        parser.add_argument('translation', type=str, help='Translation code (e.g., YLT, KJV)')

    def handle(self, *args, **options):
        translation = options['translation']

        # Path to the ZIP file
        static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'static')
        zip_path = os.path.join(static_dir, 'translations', f'{translation}.zip')

        if not os.path.exists(zip_path):
            self.stdout.write(self.style.ERROR(f'ZIP file not found: {zip_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Loading translation: {translation}'))
        self.stdout.write(f'From: {zip_path}')

        # Check if translation already exists
        existing_count = Verses.objects.filter(translation=translation).count()
        if existing_count > 0:
            self.stdout.write(self.style.WARNING(f'Translation {translation} already has {existing_count} verses in database.'))
            response = input('Do you want to delete and reload? (yes/no): ')
            if response.lower() != 'yes':
                self.stdout.write(self.style.ERROR('Aborted.'))
                return

            self.stdout.write('Deleting existing verses...')
            Verses.objects.filter(translation=translation).delete()
            self.stdout.write(self.style.SUCCESS('Deleted.'))

        # Extract and load JSON
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                json_filename = f'{translation}.json'
                with zip_ref.open(json_filename) as json_file:
                    verses_data = json.load(json_file)

                    self.stdout.write(f'Found {len(verses_data)} verses')

                    # Batch insert for better performance
                    batch_size = 1000
                    verses_to_create = []

                    for i, verse_data in enumerate(verses_data):
                        verse = Verses(
                            translation=verse_data['translation'],
                            book=verse_data['book'],
                            chapter=verse_data['chapter'],
                            verse=verse_data['verse'],
                            text=verse_data['text']
                        )
                        verses_to_create.append(verse)

                        # Insert in batches
                        if len(verses_to_create) >= batch_size:
                            Verses.objects.bulk_create(verses_to_create)
                            self.stdout.write(f'Inserted {i + 1} verses...')
                            verses_to_create = []

                    # Insert remaining verses
                    if verses_to_create:
                        Verses.objects.bulk_create(verses_to_create)

                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(verses_data)} verses!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading translation: {str(e)}'))
            raise
