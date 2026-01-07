# Ticketify Database Schema

## Overview
Ticketify is an event ticketing platform that allows users to browse events, purchase tickets, and manage their orders. Event organizers can create and manage events through an admin interface.

## Entity Relationship Diagram

```
User (Django built-in)
  |
  |-- UserProfile (1:1)
  |
  |-- Order (1:Many)
       |
       |-- OrderLineItem (1:Many)
            |
            |-- Ticket (Many:1)
                 |
                 |-- Event (Many:1)
                      |
                      |-- Category (Many:1)
```

## Models

### 1. Category
**Purpose:** Organize events into categories (e.g., Music, Sports, Theater, Conference)

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField(100) | Unique, Required |
| slug | SlugField(100) | Unique, Auto-generated |
| description | TextField | Optional |
| created_at | DateTimeField | Auto-generated |

**Relationships:**
- One Category can have Many Events

---

### 2. Event
**Purpose:** Store event information that users can buy tickets for

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | Primary Key |
| category | ForeignKey(Category) | On Delete: SET_NULL, null=True |
| title | CharField(200) | Required |
| slug | SlugField(200) | Unique, Auto-generated |
| description | TextField | Required |
| venue | CharField(200) | Required |
| address | TextField | Required |
| city | CharField(100) | Required |
| country | CharField(100) | Default='Ireland' |
| event_date | DateTimeField | Required |
| image | ImageField | Optional, placeholder if empty |
| is_active | BooleanField | Default=True |
| created_by | ForeignKey(User) | On Delete: SET_NULL, null=True |
| created_at | DateTimeField | Auto-generated |
| updated_at | DateTimeField | Auto-updated |

**Relationships:**
- Many Events belong to One Category
- One Event can have Many Tickets

---

### 3. Ticket
**Purpose:** Define ticket types for events with pricing and availability

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | Primary Key |
| event | ForeignKey(Event) | On Delete: CASCADE, related_name='tickets' |
| ticket_type | CharField(50) | Choices: General, VIP, Early Bird, Student |
| description | TextField | Optional |
| price | DecimalField | Max Digits=10, Decimal Places=2 |
| quantity_available | PositiveIntegerField | Required |
| quantity_sold | PositiveIntegerField | Default=0 |
| sale_start_date | DateTimeField | Optional |
| sale_end_date | DateTimeField | Optional |
| is_active | BooleanField | Default=True |
| created_at | DateTimeField | Auto-generated |

**Computed Properties:**
- `quantity_remaining`: quantity_available - quantity_sold
- `is_available`: Check if tickets are still available and within sale dates

**Relationships:**
- Many Tickets belong to One Event
- One Ticket type can be in Many OrderLineItems

---

### 4. UserProfile
**Purpose:** Extend Django User model with additional profile information

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | Primary Key |
| user | OneToOneField(User) | On Delete: CASCADE |
| phone_number | CharField(20) | Optional |
| street_address1 | CharField(80) | Optional |
| street_address2 | CharField(80) | Optional |
| town_or_city | CharField(40) | Optional |
| county | CharField(80) | Optional |
| postcode | CharField(20) | Optional |
| country | CharField(40) | Optional |

**Relationships:**
- One UserProfile belongs to One User

---

### 5. Order
**Purpose:** Store order information when users purchase tickets

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | Primary Key |
| order_number | CharField(32) | Unique, Auto-generated UUID |
| user_profile | ForeignKey(UserProfile) | On Delete: SET_NULL, null=True |
| full_name | CharField(50) | Required |
| email | EmailField(254) | Required |
| phone_number | CharField(20) | Required |
| date | DateTimeField | Auto-generated |
| order_total | DecimalField | Max Digits=10, Decimal Places=2 |
| stripe_pid | CharField(254) | Required |

**Relationships:**
- Many Orders can belong to One UserProfile
- One Order can have Many OrderLineItems

---

### 6. OrderLineItem
**Purpose:** Individual line items within an order (tickets purchased)

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | Primary Key |
| order | ForeignKey(Order) | On Delete: CASCADE, related_name='lineitems' |
| ticket | ForeignKey(Ticket) | On Delete: CASCADE |
| quantity | PositiveIntegerField | Required, Default=1 |
| lineitem_total | DecimalField | Max Digits=10, Decimal Places=2 |

**Relationships:**
- Many OrderLineItems belong to One Order
- Many OrderLineItems can reference One Ticket type

---

## Business Logic

### Event Management
- Events can be created, updated, and deactivated by admin users
- Events are organized by categories
- Events display remaining ticket availability

### Ticket Sales
- Ticket availability is calculated dynamically (quantity_available - quantity_sold)
- Tickets can have sale start/end dates
- Multiple ticket types can exist for one event

### Order Processing
1. User adds tickets to cart (stored in session)
2. User proceeds to checkout
3. Stripe payment is processed
4. Order is created with unique order_number
5. OrderLineItems are created for each ticket type
6. Ticket quantity_sold is incremented
7. User receives confirmation

### User Access Levels
- **Anonymous Users:** Can browse events, view details
- **Authenticated Users:** Can purchase tickets, view order history
- **Admin Users:** Full CRUD on events, tickets, categories, orders

## Data Validation Rules

### Event
- event_date must be in the future
- At least one ticket type must exist for event to be purchasable

### Ticket
- price must be >= 0
- quantity_available must be > 0
- sale_end_date must be > sale_start_date (if both provided)
- Cannot sell more tickets than quantity_available

### Order
- order_total must match sum of all lineitem_total values
- email must be valid format
- At least one OrderLineItem must exist

### OrderLineItem
- quantity must be > 0
- quantity must not exceed ticket.quantity_remaining
- lineitem_total must equal ticket.price * quantity

## Security Considerations

1. **Authentication:** Users must be authenticated to purchase tickets
2. **Authorization:** Only admin users can create/modify events
3. **Payment Security:** Use Stripe for secure payment processing
4. **Data Protection:** Sensitive data stored in environment variables
5. **CSRF Protection:** Django CSRF tokens on all forms
6. **SQL Injection:** Use Django ORM (no raw SQL queries)

## Future Enhancements (Out of Scope for MVP)
- Seat selection for venues
- QR code generation for tickets
- Email confirmations
- Refund system
- Event organizer accounts (separate from admin)
- Reviews and ratings
- Favorite/wishlist events