# Python_Project_Airbnb

# **Airbnb Clone - Django REST Framework Backend

A complete Airbnb-like booking platform backend built with Django, Django REST Framework, and MySQL.

## Features

**User Management**
- Custom user model with roles (Guest, Host, Admin)
- JWT-based authentication
- Secure password hashing

**Property Listings**
- Create, read, update, delete properties
- Filter by location, price, and availability
- Amenities support
- Image storage

**Booking System**
- Date conflict validation
- Booking status tracking (pending/confirmed/cancelled/completed)
- Guest and host management

**Reviews & Ratings**
- 1-5 star rating system
- Guest reviews for listings
- Average rating aggregation

**Messaging**
- Direct messaging between users
- Conversation threads
- Read/unread status tracking

**Payments**
- Stripe integration for secure payments
- Payment status tracking
- Refund functionality
- Webhook support

## Tech Stack

- **Backend**: Django 6.0+, Django REST Framework 3.14+
- **Database**: MySQL 8.0+
- **Authentication**: JWT (SimpleJWT)
- **Payments**: Stripe
- **Storage**: Local file system (can integrate Cloudinary)
- **Python**: 3.10+

## Project Structure

```
airbnb_backend/
├── manage.py
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
│
├── accounts/                     # User authentication
│   ├── models.py               # Custom User model
│   ├── views.py                # RegisterView, LoginView
│   ├── serializers.py          # User serializers
│   ├── urls.py                 # Auth routes
│   └── tests.py                # Auth tests
│
├── listings/                     # Property management
│   ├── models.py               # Listing, Amenity
│   ├── views.py                # ListingViewSet
│   ├── serializers.py          # ListingSerializer
│   ├── urls.py                 # Listing routes
│   └── migrations/
│
├── bookings/                     # Booking management
│   ├── models.py               # Booking with date validation
│   ├── views.py                # BookingViewSet
│   ├── serializers.py          # BookingSerializer
│   ├── urls.py                 # Booking routes
│   └── migrations/
│
├── reviews/                      # Review system
│   ├── models.py               # Review model
│   ├── views.py                # ReviewViewSet
│   ├── serializers.py          # ReviewSerializer
│   ├── urls.py                 # Review routes
│   └── migrations/
│
├── messaging/                    # Direct messaging
│   ├── models.py               # Message, Conversation
│   ├── views.py                # MessageViewSet, ConversationViewSet
│   ├── serializers.py          # Message serializers
│   ├── urls.py                 # Messaging routes
│   └── migrations/
│
├── payments/                     # Stripe payments
│   ├── models.py               # Payment model
│   ├── views.py                # PaymentViewSet with Stripe
│   ├── serializers.py          # PaymentSerializer
│   ├── urls.py                 # Payment routes
│   └── migrations/
│
└── airbnb_backend/              # Project settings
    ├── settings.py             # Django configuration
    ├── urls.py                 # Main URL routing
    ├── wsgi.py
    └── asgi.py
```

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/airbnb-clone-django.git
cd airbnb-clone-django
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create `.env` file in `airbnb_backend/` directory:
```env
DB_NAME=airbnb_project
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-django-secret-key
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
STRIPE_WEBHOOK_SECRET=whsec_your_secret
```

### 5. Create MySQL Database
```sql
CREATE DATABASE airbnb_project;
```

### 6. Run Migrations
```bash
cd airbnb_backend
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Run Server
```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`

---

## API Endpoints Overview

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user (returns JWT tokens)

### Listings
- `GET /api/listings/` - Get all listings
- `GET /api/listings/{id}/` - Get single listing
- `POST /api/listings/` - Create listing (Host only)
- `PATCH /api/listings/{id}/` - Update listing (Owner only)
- `DELETE /api/listings/{id}/` - Delete listing (Owner only)
- `GET /api/listings/my_listings/` - Get my listings (Authenticated)
- `GET /api/listings/search/` - Search with filters

### Bookings
- `GET /api/bookings/` - Get bookings (filtered by role)
- `POST /api/bookings/` - Create booking (Guest)
- `GET /api/bookings/my_bookings/` - Get my bookings (Authenticated)
- `POST /api/bookings/{id}/confirm/` - Confirm booking (Host)
- `POST /api/bookings/{id}/cancel/` - Cancel booking

### Reviews
- `GET /api/reviews/` - Get all reviews
- `POST /api/reviews/` - Create review (Guest)
- `GET /api/reviews/listing_reviews/?listing_id=1` - Get listing reviews
- `GET /api/reviews/my_reviews/` - Get my reviews (Authenticated)

### Messages
- `GET /api/messages/` - Get messages (filtered by user)
- `POST /api/messages/` - Send message (Authenticated)
- `GET /api/messages/conversation_with/?user_id=1` - Get conversation
- `GET /api/messages/unread_count/` - Get unread count (Authenticated)
- `POST /api/messages/{id}/mark_as_read/` - Mark as read

### Payments
- `GET /api/payments/` - Get payments (filtered by user)
- `POST /api/payments/{id}/process_payment/` - Process payment (Stripe)
- `POST /api/payments/{id}/refund/` - Refund payment (Host)

---

## Testing

### Test with curl
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","email":"user@example.com","password":"Pass123!","role":"guest"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"Pass123!"}'
```

### Run Django Tests
```bash
python manage.py test accounts
```

---

## Database Schema

### Users Table (`accounts_user`)
- id, username, email, password (hashed), role (guest/host/admin)
- first_name, last_name, date_joined

### Listings Table (`listings_listing`)
- id, host_id (FK), title, description, location
- price_per_night, max_guests, bedrooms, bathrooms
- is_available, image, created_at, updated_at

### Bookings Table (`bookings_booking`)
- id, guest_id (FK), listing_id (FK)
- check_in_date, check_out_date, number_of_guests
- total_price, status, created_at

### Reviews Table (`reviews_review`)
- id, guest_id (FK), listing_id (FK)
- rating (1-5), comment, created_at

### Messages Table (`messaging_message`)
- id, sender_id (FK), receiver_id (FK)
- content, is_read, created_at

### Payments Table (`payments_payment`)
- id, booking_id (FK), amount
- status, stripe_payment_intent, transaction_id
- created_at, updated_at

---

## Key Features Explained

### Role-Based Access
- **Guest**: Can search, book, review, message
- **Host**: Can create listings, confirm/respond to bookings
- **Admin**: Full access via Django admin

### Date Conflict Validation
Bookings automatically check for overlapping dates:
```python
# Prevents double-booking
if date conflict:
    raise ValidationError("Dates conflict with existing booking")
```

### Stripe Integration
Secure payment processing with test mode:
- Test cards: `tok_visa`, `tok_mastercard`
- Production: Real Stripe API keys required

### JWT Authentication
All authenticated endpoints require:
```
Authorization: Bearer <access_token>
```

---

## Common Workflows

### Host Listing a Property
1. Register → Login (as host)
2. Create Listing → Add amenities
3. Wait for bookings
4. Confirm bookings → Receive payments

### Guest Booking Property
1. Register → Login (as guest)
2. Search listings
3. Create booking
4. Pay with Stripe
5. Check-in → Leave review
6. Send message to host

### Payment Flow
1. Guest creates booking
2. Payment record created automatically
3. Guest processes payment with Stripe
4. Host receives confirmation
5. Booking status → confirmed

---

## Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use environment variables for secrets
- [ ] Configure CORS if needed
- [ ] Set up HTTPS/SSL
- [ ] Use production database
- [ ] Configure static/media file serving
- [ ] Set up logging
- [ ] Use Gunicorn + Nginx

### Deploy to AWS EC2
```bash
# Install Python, venv, MySQL
# Clone repo, install dependencies
# Run migrations
# Start with Gunicorn
gunicorn airbnb_backend.wsgi:application --bind 0.0.0.0:8000
```

---

## Future Enhancements

- [ ] React/Next.js frontend
- [ ] Real-time chat with WebSockets
- [ ] Advanced search with ElasticSearch
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Cloudinary image storage
- [ ] Two-factor authentication
- [ ] Review moderation system
- [ ] Host verification system

---

## Troubleshooting

### Database Connection Error
```
ERROR 2003: Can't connect to MySQL server
```
→ Check MySQL is running: `mysql -u root -p`

### Migration Error
```
django.db.utils.ProgrammingError: no such table
```
→ Run: `python manage.py migrate`

### Authentication Error (401)
```
"detail": "Authentication credentials were not provided."
```
→ Add Authorization header with valid token

### Permission Error (403)
```
"error": "You can only edit your own listings"
```
→ Ensure you're the owner or have proper role

---

## License

This project is for educational purposes. Feel free to use and modify for learning.

---

## Contact & Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Contact: [hariyogeshram0905@gmail.com]

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-01  
**Python**: 3.10+  
**Django**: 6.0+
