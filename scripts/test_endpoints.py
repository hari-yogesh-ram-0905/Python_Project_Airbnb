import time
import json

try:
    import requests
except Exception:
    print("The 'requests' library is required. Install with: pip install requests")
    raise

BASE = 'http://localhost:8000'
HEADERS = {'Content-Type': 'application/json'}

def pretty(resp):
    print('---')
    print(resp.status_code, resp.reason)
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text)
    print('---\n')

# 1. Register
username = f'testuser_{int(time.time())}'
register_payload = {
    'username': username,
    'email': f'{username}@example.com',
    'password': 'TestPass123!'
}
print('Registering user:', username)
r = requests.post(f'{BASE}/api/auth/register/', headers=HEADERS, json=register_payload)
pretty(r)
if r.status_code not in (200,201):
    print('Register failed, aborting further tests')
    raise SystemExit(1)
user = r.json()
user_id = user.get('id') or user.get('pk')

# 2. Login
login_payload = {'username': username, 'password': 'TestPass123!'}
print('Logging in as:', username)
r = requests.post(f'{BASE}/api/auth/login/', headers=HEADERS, json=login_payload)
pretty(r)
if r.status_code not in (200,201):
    print('Login failed, aborting')
    raise SystemExit(1)
tokens = r.json()
access = tokens.get('access')
if not access:
    print('No access token returned; aborting')
    raise SystemExit(1)
user = tokens.get('user', {})
user_id = user.get('id')
AUTH = {'Authorization': f'Bearer {access}', 'Content-Type': 'application/json'}

# 2.5 Fetch existing amenities
print('Fetching amenities...')
amenity_ids = []
r = requests.get(f'{BASE}/api/listings/amenities/', headers=HEADERS)
if r.status_code == 200:
    amenities_data = r.json()
    amenities = amenities_data if isinstance(amenities_data, list) else amenities_data.get('results', [])
    for amenity in amenities[:2]:  # Use first 2 amenities
        aid = amenity.get('id')
        if aid:
            amenity_ids.append(aid)
            print(f'  Found amenity id={aid}: {amenity.get("name")}')

print(f'Using amenity IDs: {amenity_ids if amenity_ids else "[1, 2] (fallback)"}\n')

# 3. List properties (unauthenticated)
print('GET /api/listings/ (unauthenticated)')
r = requests.get(f'{BASE}/api/listings/')
pretty(r)

# 4. Create listing (authenticated)
listing_payload = {
    'title':'Cozy Studio',
    'description':'Nice studio downtown',
    'location':'123 Main St, Anytown',
    'price_per_night':45.0,
    'max_guests':2,
    'bedrooms':1,
    'bathrooms':1,
    'amenity_ids':amenity_ids if amenity_ids else [1, 2],
}
print('Creating listing (authenticated)')
r = requests.post(f'{BASE}/api/listings/', headers=AUTH, json=listing_payload)
pretty(r)
if r.status_code in (200,201):
    listing = r.json()
    listing_id = listing.get('id')
else:
    listing_id = None

# 5. GET listings (authenticated)
print('GET /api/listings/ (authenticated)')
r = requests.get(f'{BASE}/api/listings/', headers=AUTH)
pretty(r)

# 6. Book property (if listing created)
if listing_id:
    from datetime import datetime, timedelta
    today = datetime.now()
    start = today.strftime('%Y-%m-%d')
    end = (today + timedelta(days=5)).strftime('%Y-%m-%d')
    booking_payload = {
        'listing': listing_id,
        'check_in_date': start,
        'check_out_date': end,
        'number_of_guests': 2,
        'total_price': 225.00  # 5 nights * $45/night
    }
    print('Creating booking for listing', listing_id)
    r = requests.post(f'{BASE}/api/bookings/', headers=AUTH, json=booking_payload)
    pretty(r)
    if r.status_code in (200,201):
        booking = r.json()
        booking_id = booking.get('id')
    else:
        booking_id = None
else:
    print('No listing created: skipping booking')
    booking_id = None

# 7. Leave review (if listing exists)
if listing_id:
    review_payload = {'listing': listing_id, 'rating':5, 'comment':'Great stay!'}
    print('Posting review for listing', listing_id)
    r = requests.post(f'{BASE}/api/reviews/', headers=AUTH, json=review_payload)
    pretty(r)
else:
    print('No listing created: skipping review')

# 8. Send message (to self)
if user_id:
    msg_payload = {'receiver': user_id, 'content':'Hello from test script'}
    print('Sending message to user id', user_id)
    r = requests.post(f'{BASE}/api/messages/', headers=AUTH, json=msg_payload)
    pretty(r)
else:
    print('No user id found: skipping message')

# 9. Process payment (create payment for booking, then process it)
# First, try to get/create a payment for the booking
if booking_id:
    # Try to create a payment via POST to /api/payments/
    print('Creating payment for booking', booking_id)
    payment_payload = {
        'booking': booking_id,
        'amount': 225.00,
        'status': 'pending'
    }
    r = requests.post(f'{BASE}/api/payments/', headers=AUTH, json=payment_payload)
    pretty(r)
    if r.status_code in (200,201):
        payment = r.json()
        payment_id = payment.get('id')
    else:
        payment_id = None

    # If payment created, try to process it
    if payment_id:
        print('Processing payment id', payment_id)
        # Use a Stripe test token: tok_visa (requires account and test mode)
        pay_payload = {'stripe_token': 'tok_visa'}
        r = requests.post(f'{BASE}/api/payments/{payment_id}/process_payment/', headers=AUTH, json=pay_payload)
        pretty(r)
    else:
        print('No payment created: skipping process_payment')
elif 1:  # Fallback: try payment id 1
    print('Attempting to process payment for id 1')
    pay_payload = {'stripe_token': 'tok_visa'}
    r = requests.post(f'{BASE}/api/payments/1/process_payment/', headers=AUTH, json=pay_payload)
    pretty(r)

print('Tests complete')
