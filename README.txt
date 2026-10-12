LITTLE LEMON RESTAURANT API - DJANGO REST FRAMEWORK CAPSTONE PROJECT
=====================================================================

PROJECT SETUP INSTRUCTIONS
---------------------------

1. Create MySQL Database:
   mysql -u root -p
   CREATE DATABASE littlelemon;
   EXIT;

2. Update Database Credentials (if needed):
   Edit littlelemon/settings.py and update DATABASES section with your MySQL username/password

3. Install Dependencies:
   cd littlelemon
   pipenv shell
   pipenv install

4. Run Migrations:
   python manage.py makemigrations
   python manage.py migrate

5. Create Superuser (for admin access):
   python manage.py createsuperuser

6. Run Server:
   python manage.py runserver

7. Run Tests:
   python manage.py test restaurant


API ENDPOINTS FOR TESTING
==========================

AUTHENTICATION ENDPOINTS:
-------------------------
POST   /auth/users/                    - Register a new user
POST   /auth/token/login/              - Login and get authentication token
POST   /auth/token/logout/             - Logout (requires authentication)
GET    /auth/users/me/                 - Get current user info (requires authentication)


MENU API ENDPOINTS (Requires Authentication):
----------------------------------------------
GET    /api/menu/                      - List all menu items (paginated)
GET    /api/menu/{id}/                 - Get single menu item details
POST   /api/menu/                      - Create new menu item
PUT    /api/menu/{id}/                 - Update menu item (full update)
PATCH  /api/menu/{id}/                 - Partially update menu item
DELETE /api/menu/{id}/                 - Delete menu item


BOOKING API ENDPOINTS (Requires Authentication):
-------------------------------------------------
GET    /api/bookings/                  - List all table bookings (paginated)
GET    /api/bookings/{id}/             - Get single booking details
POST   /api/bookings/                  - Create new table booking
PUT    /api/bookings/{id}/             - Update booking (full update)
PATCH  /api/bookings/{id}/             - Partially update booking
DELETE /api/bookings/{id}/             - Delete booking


OTHER ENDPOINTS:
----------------
GET    /api/user/                      - Get current user profile (requires authentication)
GET    /admin/                         - Django admin panel
GET    /api-auth/login/                - Browsable API login page


TESTING WITH INSOMNIA REST CLIENT
==================================

Step 1: Register a User
-----------------------
Request: POST http://127.0.0.1:8000/auth/users/
Body (JSON):
{
  "username": "testuser",
  "password": "testpass123",
  "email": "test@example.com"
}


Step 2: Get Authentication Token
---------------------------------
Request: POST http://127.0.0.1:8000/auth/token/login/
Body (JSON):
{
  "username": "testuser",
  "password": "testpass123"
}

Response will contain:
{
  "auth_token": "your-token-here"
}

IMPORTANT: Copy this token for use in subsequent requests!


Step 3: Set Authorization Header
---------------------------------
For all authenticated requests, add this header:
Authorization: Token your-token-here


Step 4: Test Menu API
----------------------
CREATE Menu Item:
POST http://127.0.0.1:8000/api/menu/
Headers: Authorization: Token your-token-here
Body (JSON):
{
  "title": "Greek Salad",
  "price": 12.99,
  "inventory": 50
}

LIST Menu Items:
GET http://127.0.0.1:8000/api/menu/
Headers: Authorization: Token your-token-here

GET Single Menu Item:
GET http://127.0.0.1:8000/api/menu/1/
Headers: Authorization: Token your-token-here

UPDATE Menu Item:
PUT http://127.0.0.1:8000/api/menu/1/
Headers: Authorization: Token your-token-here
Body (JSON):
{
  "title": "Greek Salad Updated",
  "price": 13.99,
  "inventory": 45
}

PARTIAL UPDATE Menu Item:
PATCH http://127.0.0.1:8000/api/menu/1/
Headers: Authorization: Token your-token-here
Body (JSON):
{
  "price": 14.99
}

DELETE Menu Item:
DELETE http://127.0.0.1:8000/api/menu/1/
Headers: Authorization: Token your-token-here


Step 5: Test Booking API
-------------------------
CREATE Booking:
POST http://127.0.0.1:8000/api/bookings/
Headers: Authorization: Token your-token-here
Body (JSON):
{
  "first_name": "John",
  "reservation_date": "2024-12-15",
  "reservation_slot": 18
}

LIST Bookings:
GET http://127.0.0.1:8000/api/bookings/
Headers: Authorization: Token your-token-here

GET Single Booking:
GET http://127.0.0.1:8000/api/bookings/1/
Headers: Authorization: Token your-token-here

UPDATE Booking:
PUT http://127.0.0.1:8000/api/bookings/1/
Headers: Authorization: Token your-token-here
Body (JSON):
{
  "first_name": "John Updated",
  "reservation_date": "2024-12-15",
  "reservation_slot": 19
}

DELETE Booking:
DELETE http://127.0.0.1:8000/api/bookings/1/
Headers: Authorization: Token your-token-here


EXPECTED RESPONSES
==================

Success Status Codes:
- 200 OK: GET, PUT, PATCH requests
- 201 Created: POST requests (resource created)
- 204 No Content: DELETE requests (successful deletion)

Error Status Codes:
- 400 Bad Request: Invalid data
- 401 Unauthorized: Missing or invalid authentication token
- 404 Not Found: Resource doesn't exist


FEATURES IMPLEMENTED
====================

✓ Django REST Framework for API development
✓ MySQL database connection
✓ User registration and authentication (Token-based)
✓ Menu API with full CRUD operations (GET, POST, PUT, PATCH, DELETE)
✓ Booking/Table Reservation API with full CRUD operations
✓ Token authentication required for all API endpoints
✓ Comprehensive unit tests (run: python manage.py test)
✓ Django admin panel for data management
✓ Static HTML pages for booking form
✓ Pagination for list endpoints
✓ RESTful API design principles


PROJECT STRUCTURE
=================

littlelemon/              - Django project directory
  settings.py             - Project settings with REST Framework config
  urls.py                 - Main URL routing with auth endpoints

restaurant/               - Django app
  models.py               - Menu and Booking models
  serializers.py          - DRF serializers for API
  views.py                - ViewSets for Menu and Booking APIs
  urls.py                 - App URL routing with API router
  tests.py                - Comprehensive unit tests
  admin.py                - Admin panel configuration
  migrations/             - Database migrations
  templates/              - HTML templates
  static/                 - CSS and JavaScript files

Pipfile                   - Dependencies (Django, DRF, MySQL, Djoser)
README.txt                - This file


GRADING CHECKLIST
=================

✓ Django serves static HTML content (home, about, book pages)
✓ Project committed to Git repository
✓ Backend connects to MySQL database
✓ Menu API implemented with all CRUD operations
✓ Table booking API implemented with all CRUD operations
✓ User registration and authentication set up
✓ Unit tests included and passing
✓ API can be tested with Insomnia REST client


TROUBLESHOOTING
===============

If you get "Access denied" error:
- Update MySQL credentials in littlelemon/settings.py

If you get "No module named 'rest_framework'":
- Run: pipenv install

If tests fail:
- Ensure migrations are run: python manage.py migrate
- Check MySQL is running and database exists


CONTACT & SUBMISSION
====================

This project is ready for peer review.
All API endpoints are functional and tested.
Authentication is properly configured.
Unit tests are comprehensive and passing.

Happy Testing!
