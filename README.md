# Ticketify

A professional event ticketing platform built with Django that allows users to browse events, purchase tickets, and manage their bookings with secure Stripe payment integration.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [User Experience Design](#user-experience-design)
- [Technologies Used](#technologies-used)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

## Project Overview

Ticketify is a full-stack web application that provides a seamless ticket booking experience for event-goers. Users can browse upcoming events, filter by category or location, view detailed event information, and securely purchase tickets using Stripe payment processing.

### Purpose

The platform addresses the need for a reliable, user-friendly ticket booking system that:
- Provides real-time ticket availability tracking
- Ensures secure payment processing
- Offers an intuitive interface for event discovery
- Manages venue capacity effectively
- Delivers a professional booking experience

## Features

### Implemented Features

#### User Authentication
- User registration with email validation
- Secure login/logout functionality
- User profile management
- Order history tracking

#### Event Management
- Browse all upcoming events
- Search events by title or description
- Filter by category (Music, Sports, Arts, Comedy, etc.)
- Filter by city/location
- View detailed event information including:
  - Event date, time, and venue
  - Ticket types and pricing
  - Venue capacity and availability
  - Event description and location details

#### Shopping Cart
- Session-based cart functionality
- Add/remove tickets
- Update ticket quantities
- Real-time availability validation
- Cart persistence across sessions

#### Payment Processing
- Secure Stripe payment integration
- Multiple ticket type support (Standard, VIP, Early Bird)
- Payment confirmation
- Order tracking with unique order numbers
- Webhook integration for payment verification

#### Responsive Design
- Mobile-first approach using Tailwind CSS
- Clean, professional interface
- Intuitive navigation
- Accessible design patterns

### Future Features

- Email notifications for order confirmations
- QR code ticket generation
- Event organizer dashboard
- Ticket transfer functionality
- Reviews and ratings system
- Recurring events support
- Multiple payment methods
- Wishlist functionality

## User Experience Design

### Design Philosophy

The design prioritizes simplicity, clarity, and ease of use. Key UX decisions include:

#### Color Scheme
- Primary: Indigo (#4F46E5) - Conveys trust and professionalism
- Secondary: Purple gradients - Creates visual interest
- Neutral: Gray scale - Ensures readability
- Success: Green - Positive feedback
- Error: Red - Clear error communication

#### Typography
- System font stack for optimal performance
- Clear hierarchy with consistent heading sizes
- Adequate line spacing for readability

#### Navigation
- Persistent navigation bar with cart indicator
- Breadcrumb navigation on detail pages
- Clear call-to-action buttons
- Sticky cart summary on checkout

#### User Flows

**Browsing Events:**
Home → Events List → Filter/Search → Event Detail → Add to Cart

**Checkout Process:**
Cart → Checkout (Billing Info) → Payment (Stripe) → Confirmation

**Account Management:**
Register/Login → Profile → View Orders

### Accessibility Considerations

- Semantic HTML structure
- Color contrast compliance
- Keyboard navigation support
- Screen reader friendly labels
- Form validation with clear error messages

## Technologies Used

### Backend
- **Django 6.0.1** - Python web framework
- **Python 3.x** - Programming language
- **PostgreSQL** - Production database (via Neon)
- **SQLite** - Development database
- **Stripe 14.1.0** - Payment processing

### Frontend
- **Tailwind CSS 3.4.1** - Utility-first CSS framework
- **HTML5** - Markup language
- **JavaScript** - Client-side interactivity

### Dependencies
- **gunicorn** - WSGI HTTP server
- **whitenoise** - Static file serving
- **python-decouple** - Environment variable management
- **dj-database-url** - Database configuration
- **psycopg2-binary** - PostgreSQL adapter
- **Pillow** - Image processing

### Development Tools
- **Git** - Version control
- **npm** - Package management for Tailwind
- **VS Code** - Code editor

## Database Schema

The application uses a relational database with the following main models:

### Core Models

**Category**
- Event categorization (Music, Sports, Arts, etc.)
- Auto-generated slugs for URLs

**Event**
- Event details (title, description, date, venue)
- Capacity tracking
- Category relationship
- Location information

**Ticket**
- Ticket types (Standard, VIP, Early Bird)
- Pricing and quantity management
- Availability tracking
- Event relationship

**Order**
- User purchase records
- Unique order numbers (UUID)
- Billing information
- Payment status tracking
- Stripe integration

**OrderLineItem**
- Individual ticket purchases
- Quantity and pricing
- Order relationship

**UserProfile**
- Extended user information
- Address details
- Order history

For detailed schema documentation, see [SCHEMA.md](SCHEMA.md).

### Database Relationships

- One-to-Many: Category → Events
- One-to-Many: Event → Tickets
- One-to-Many: User → Orders
- One-to-Many: Order → OrderLineItems
- One-to-One: User → UserProfile

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js and npm (for Tailwind CSS)
- PostgreSQL (for production)

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Ticketify
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tailwind CSS:
```bash
npm install
```

5. Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
ALLOWED_HOSTS=localhost,127.0.0.1
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-webhook-secret
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Build Tailwind CSS:
```bash
npm run build
```

9. Collect static files:
```bash
python manage.py collectstatic
```

10. Run the development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to view the application.

## Configuration

### Environment Variables

Required environment variables:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `STRIPE_PUBLIC_KEY`: Stripe publishable key
- `STRIPE_SECRET_KEY`: Stripe secret key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook signing secret

### Stripe Configuration

1. Create a Stripe account at https://stripe.com
2. Get your API keys from the Stripe Dashboard
3. Add the keys to your `.env` file
4. Set up a webhook endpoint pointing to `/tickets/webhook/`
5. Configure the webhook to listen for `payment_intent.succeeded` events

## Usage

### Admin Panel

Access the Django admin at `/admin` to:
- Create and manage events
- Add ticket types and pricing
- View orders and payments
- Manage categories
- Monitor user accounts

### Customer Workflow

1. **Browse Events**: View all available events on the homepage or events page
2. **Search/Filter**: Use the search bar or category filters to find specific events
3. **View Details**: Click on an event to see full details and ticket options
4. **Add to Cart**: Select ticket type and quantity, then add to cart
5. **Checkout**: Review cart and proceed to checkout
6. **Payment**: Enter billing information and complete payment via Stripe
7. **Confirmation**: Receive order confirmation and view order details

### Development Workflow

Watch for Tailwind CSS changes during development:
```bash
npm run watch:css
```

Build for production:
```bash
npm run build
```

## Testing

### Manual Testing

Test cases should cover:

1. **User Authentication**
   - Registration with valid/invalid data
   - Login/logout functionality
   - Profile updates

2. **Event Browsing**
   - Search functionality
   - Category filtering
   - City filtering
   - Event detail views

3. **Cart Operations**
   - Adding tickets
   - Updating quantities
   - Removing items
   - Quantity validation

4. **Checkout Process**
   - Form validation
   - Stripe payment flow
   - Order creation
   - Payment confirmation

5. **Responsive Design**
   - Mobile view
   - Tablet view
   - Desktop view

### Automated Testing

Run Django tests:
```bash
python manage.py test
```

### Code Validation

- Python: PEP 8 compliance
- HTML: W3C Markup Validation
- CSS: W3C CSS Validation
- JavaScript: ESLint

## Deployment

### Heroku Deployment

1. Install Heroku CLI and login:
```bash
heroku login
```

2. Create a Heroku app:
```bash
heroku create your-app-name
```

3. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:mini
```

4. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set STRIPE_PUBLIC_KEY=your-key
heroku config:set STRIPE_SECRET_KEY=your-key
heroku config:set STRIPE_WEBHOOK_SECRET=your-key
```

5. Deploy:
```bash
git push heroku main
```

6. Run migrations:
```bash
heroku run python manage.py migrate
```

7. Create superuser:
```bash
heroku run python manage.py createsuperuser
```

8. Collect static files:
```bash
heroku run python manage.py collectstatic
```

### Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure allowed hosts
- [ ] Set up PostgreSQL database
- [ ] Configure Stripe webhook endpoint
- [ ] Enable HTTPS
- [ ] Set strong SECRET_KEY
- [ ] Configure email backend
- [ ] Set up monitoring
- [ ] Create backup strategy

## Credits

### Technologies
- Django: https://www.djangoproject.com/
- Tailwind CSS: https://tailwindcss.com/
- Stripe: https://stripe.com/
- PostgreSQL: https://www.postgresql.org/

### Developer
- Built by: Brandon Lea
- Project: Code Institute Level 5 Diploma Project
- Year: 2026

### Acknowledgments
- Code Institute for project requirements and guidance
- Stripe documentation for payment integration
- Django documentation for framework guidance
- Tailwind CSS for design system