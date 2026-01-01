import requests, json, sys
BASE='http://127.0.0.1:8000'
# change these if you prefer another test user
login_payload = {'username':'testuser_1767034231','password':'TestPass123!'}
print('LOGIN REQUEST ->', BASE + '/api/auth/login/')
try:
    r = requests.post(BASE + '/api/auth/login/', json=login_payload, timeout=10)
    print('\nLOGIN STATUS:', r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print(r.text)
except Exception as e:
    print('Login request failed:', e)
    sys.exit(1)

access = None
if r.status_code in (200,201):
    access = r.json().get('access')
if not access:
    print('\nNo access token returned; aborting my_listings call')
    sys.exit(0)

headers = {'Authorization': f'Bearer {access}', 'Content-Type':'application/json'}
print('\nMY_LISTINGS REQUEST ->', BASE + '/api/listings/my_listings/')
try:
    r2 = requests.get(BASE + '/api/listings/my_listings/', headers=headers, timeout=10)
    print('\nMY_LISTINGS STATUS:', r2.status_code)
    try:
        print(json.dumps(r2.json(), indent=2))
    except Exception:
        print(r2.text)
except Exception as e:
    print('My listings request failed:', e)
    sys.exit(1)
