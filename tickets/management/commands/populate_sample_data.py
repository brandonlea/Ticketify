from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files.base import ContentFile
from datetime import timedelta
from decimal import Decimal
from events.models import Category, Event
from tickets.models import Ticket
import random
import requests


class Command(BaseCommand):
    help = 'Populate database with sample categories, cities, and events'

    def download_image(self, url, filename):
        """Download image from URL and return ContentFile"""
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return ContentFile(response.content, name=filename)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  Failed to download image: {e}'))
        return None

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create Categories
        categories_data = [
            {'name': 'Concerts', 'slug': 'concerts'},
            {'name': 'Sports', 'slug': 'sports'},
            {'name': 'Theatre', 'slug': 'theatre'},
            {'name': 'Comedy', 'slug': 'comedy'},
            {'name': 'Festivals', 'slug': 'festivals'},
            {'name': 'Family', 'slug': 'family'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Cities
        cities = ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Leeds', 'Glasgow', 'Edinburgh', 'Dublin', 'Bristol', 'Newcastle']
        venues_by_city = {
            'London': ['O2 Arena', 'Wembley Stadium', 'Royal Albert Hall', 'SSE Arena'],
            'Manchester': ['AO Arena', 'Old Trafford', 'Manchester Arena', 'Albert Hall'],
            'Birmingham': ['Utilita Arena', 'Symphony Hall', 'NEC Birmingham'],
            'Liverpool': ['M&S Bank Arena', 'Anfield Stadium', 'Liverpool Empire'],
            'Leeds': ['First Direct Arena', 'Leeds Arena', 'Elland Road'],
            'Glasgow': ['OVO Hydro', 'Celtic Park', 'SEC Armadillo'],
            'Edinburgh': ['Usher Hall', 'Edinburgh Playhouse', 'Murrayfield Stadium'],
            'Dublin': ['3Arena', 'Aviva Stadium', 'Olympia Theatre'],
            'Bristol': ['Bristol Beacon', 'Ashton Gate Stadium', 'Colston Hall'],
            'Newcastle': ['Utilita Arena Newcastle', "St James' Park", 'Newcastle City Hall'],
        }

        # Sample Events Data
        events_data = [
            # Concerts
            {
                'title': 'Arctic Monkeys Live',
                'category': 'concerts',
                'description': 'Join Arctic Monkeys for an unforgettable night of indie rock classics and new hits. Experience their electrifying performance live.',
                'image_url': 'https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?w=800&q=80',
                'days_offset': 45,
            },
            {
                'title': 'Ed Sheeran World Tour',
                'category': 'concerts',
                'description': 'Ed Sheeran brings his Mathematics Tour to the UK. Don\'t miss this incredible solo performance.',
                'image_url': 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800&q=80',
                'days_offset': 60,
            },
            {
                'title': 'Taylor Swift - The Eras Tour',
                'category': 'concerts',
                'description': 'Experience the magic of Taylor Swift performing hits from across her entire career in this spectacular show.',
                'image_url': 'https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800&q=80',
                'days_offset': 30,
            },
            {
                'title': 'Coldplay Music of the Spheres',
                'category': 'concerts',
                'description': 'Coldplay\'s stunning visual and musical spectacle featuring their greatest hits and latest album.',
                'image_url': 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&q=80',
                'days_offset': 90,
            },

            # Sports
            {
                'title': 'Premier League: Manchester United vs Liverpool',
                'category': 'sports',
                'description': 'The biggest rivalry in English football. Watch these two giants battle it out at Old Trafford.',
                'image_url': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800&q=80',
                'days_offset': 21,
            },
            {
                'title': 'Six Nations Rugby: England vs Ireland',
                'category': 'sports',
                'description': 'International rugby at its finest. Two powerhouses clash in this crucial Six Nations match.',
                'image_url': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800&q=80',
                'days_offset': 35,
            },
            {
                'title': 'Champions League Final',
                'category': 'sports',
                'description': 'The pinnacle of European club football. Be there to witness history in the making.',
                'image_url': 'https://images.unsplash.com/photo-1459865264687-595d652de67e?w=800&q=80',
                'days_offset': 120,
            },

            # Theatre
            {
                'title': 'Hamilton',
                'category': 'theatre',
                'description': 'The revolutionary musical phenomenon returns. Don\'t miss this award-winning Broadway sensation.',
                'image_url': 'https://images.unsplash.com/photo-1503095396549-807759245b35?w=800&q=80',
                'days_offset': 14,
            },
            {
                'title': 'The Phantom of the Opera',
                'category': 'theatre',
                'description': 'Andrew Lloyd Webber\'s timeless masterpiece. Experience the romance and mystery of this classic musical.',
                'image_url': 'https://images.unsplash.com/photo-1507924538820-ede94a04019d?w=800&q=80',
                'days_offset': 28,
            },
            {
                'title': 'Les Misérables',
                'category': 'theatre',
                'description': 'The world\'s longest-running musical. A tale of passion, sacrifice and redemption.',
                'image_url': 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=800&q=80',
                'days_offset': 42,
            },

            # Comedy
            {
                'title': 'Michael McIntyre: Macnificent',
                'category': 'comedy',
                'description': 'Britain\'s biggest comedian returns with his hilarious new show. Guaranteed laughs all night.',
                'image_url': 'https://images.unsplash.com/photo-1585699324551-f6c309eedeca?w=800&q=80',
                'days_offset': 25,
            },
            {
                'title': 'Russell Howard: Respite',
                'category': 'comedy',
                'description': 'Russell Howard brings his unique brand of comedy to your city. An evening of laughs guaranteed.',
                'image_url': 'https://images.unsplash.com/photo-1527224857830-43a7acc85260?w=800&q=80',
                'days_offset': 40,
            },

            # Festivals
            {
                'title': 'Glastonbury Festival',
                'category': 'festivals',
                'description': '5 days of music, dance, comedy, theatre, circus, cabaret and more. The world\'s most famous festival.',
                'image_url': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800&q=80',
                'days_offset': 150,
            },
            {
                'title': 'Reading Festival',
                'category': 'festivals',
                'description': 'Three days of the biggest names in rock, indie and alternative music.',
                'image_url': 'https://images.unsplash.com/photo-1506157786151-b8491531f063?w=800&q=80',
                'days_offset': 130,
            },

            # Family
            {
                'title': 'Disney on Ice: Frozen',
                'category': 'family',
                'description': 'Let it go and join Elsa, Anna and friends in this magical ice skating spectacular.',
                'image_url': 'https://images.unsplash.com/photo-1576085898323-218337e3e43c?w=800&q=80',
                'days_offset': 20,
            },
            {
                'title': 'The Lion King',
                'category': 'family',
                'description': 'Disney\'s award-winning musical brings the Pride Lands to life. Perfect for the whole family.',
                'image_url': 'https://images.unsplash.com/photo-1514306191717-452ec28c7814?w=800&q=80',
                'days_offset': 35,
            },
        ]

        # Create Events
        for i, event_data in enumerate(events_data, 1):
            city = random.choice(cities)
            venue = random.choice(venues_by_city[city])
            event_date = timezone.now() + timedelta(days=event_data['days_offset'])

            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    'category': categories[event_data['category']],
                    'description': event_data['description'],
                    'event_date': event_date,
                    'venue': venue,
                    'address': f'{venue}, {city}',
                    'city': city,
                    'country': 'United Kingdom' if city != 'Dublin' else 'Ireland',
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created event: {event.title}'))

                # Download and save image
                image_file = self.download_image(
                    event_data['image_url'],
                    f'event_{i}.jpg'
                )
                if image_file:
                    event.image.save(f'event_{i}.jpg', image_file, save=True)
                    self.stdout.write(self.style.SUCCESS(f'  Downloaded image for {event.title}'))

                # Create tickets for the event
                ticket_types = [
                    ('general', Decimal('45.00'), 500),
                    ('vip', Decimal('120.00'), 100),
                    ('student', Decimal('35.00'), 150),
                ]

                for ticket_type, price, quantity in ticket_types:
                    # Randomly sell some tickets
                    sold = random.randint(0, int(quantity * 0.3))

                    Ticket.objects.create(
                        event=event,
                        ticket_type=ticket_type,
                        price=price,
                        quantity_available=quantity,
                        quantity_sold=sold,
                    )

                self.stdout.write(self.style.SUCCESS(f'  Created tickets for {event.title}'))

        self.stdout.write(self.style.SUCCESS('\nSample data population complete!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories_data)} categories'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(events_data)} events with tickets'))
