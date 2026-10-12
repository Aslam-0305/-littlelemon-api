# Little Lemon Restaurant Booking System

A full-stack Django application for managing restaurant table reservations with a MySQL database backend and JavaScript frontend.

## Project Structure

```
littlelemon/                    # Django project directory
├── settings.py                 # Project settings with MySQL configuration
├── urls.py                     # Main URL configuration
├── wsgi.py                     # WSGI configuration
└── asgi.py                     # ASGI configuration

restaurant/                     # Django app directory
├── models.py                   # Booking model with unique constraint
├── views.py                    # API endpoints and page views
├── urls.py                     # App URL patterns
├── admin.py                    # Admin panel configuration
├── migrations/                 # Database migrations
│   ├── __init__.py
│   └── 0001_initial.py
├── templates/                  # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── book.html
│   └── reservations.html
└── static/                     # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── book.js             # Booking form JavaScript with Fetch API

manage.py                       # Django management script
Pipfile                         # Pipenv dependencies
```

## Features Implemented

### ✅ Required Features (Per Grading Criteria)

1. **App Installation**: Restaurant app is added to `INSTALLED_APPS` in settings.py
2. **Database Configuration**: MySQL database configured in settings.py
3. **Migrations**: Initial migration file created for Booking model
4. **Booking Form Fields**: Three required fields implemented:
   - First Name (text input)
   - Reservation Date (date selector)
   - Reservation Slot (dropdown with time slots)
5. **Date Selector**: Date picker opens when clicking the reservation date field
6. **JSON Data Display**: All bookings available as JSON on `/reservations/` page
7. **Duplicate Booking Prevention**: Unique constraint prevents duplicate bookings for same date/time
8. **Dynamic Date Refresh**: Changing the date automatically refreshes booking data
9. **Unavailable Slots**: Booked time slots are disabled and shown as grey
10. **API Date Filtering**: Bookings API supports date parameter (e.g., `/bookings/?date=2022-12-13`)
11. **No Booking Message**: Shows "No bookings for [date]" when no reservations exist
12. **Fetch API**: JavaScript uses Fetch API to retrieve and submit data
13. **Current Date Default**: Booking form automatically selects current date on page load

## Setup Instructions for Peer Reviewers

### Prerequisites

- Python 3.x installed
- MySQL server installed and running
- pipenv installed (`pip install pipenv`)

### Step 1: Create MySQL Database

Before running the project, create a MySQL database:

```sql
mysql -u root -p
CREATE DATABASE littlelemon;
EXIT;
```

### Step 2: Update Database Credentials (If Needed)

If your MySQL username/password differs from the defaults, update `littlelemon/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'littlelemon',
        'USER': 'root',              # Change if different
        'PASSWORD': 'password',      # Change to your MySQL password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### Step 3: Install Dependencies and Run Migrations

```bash
# Navigate to project directory
cd littlelemon

# Create virtual environment and install dependencies
pipenv shell
pipenv install

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

### Step 5: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: http://127.0.0.1:8000/

## Optional: Load Sample Data

To load sample bookings for testing:

```bash
python manage.py loaddata restaurant/fixtures/sample_bookings.json
```

This will create 5 sample bookings across different dates.

## Running Tests

The project includes automated tests. To run them:

```bash
python manage.py test restaurant
```

Tests cover:
- Model creation and constraints
- API endpoints (GET/POST)
- Duplicate booking prevention
- Date filtering

## Testing the Application

### Pages to Test

1. **Home Page**: http://127.0.0.1:8000/
   - Basic landing page with navigation

2. **About Page**: http://127.0.0.1:8000/about/
   - Restaurant information

3. **Book Page**: http://127.0.0.1:8000/book/
   - Main booking form
   - Test Features:
     - ✓ Current date is automatically selected
     - ✓ Click on date field to open date picker
     - ✓ Select a date to see current reservations for that date
     - ✓ Create a booking with first name, date, and time slot
     - ✓ Try to book the same slot again - should show error
     - ✓ Booked time slots become grey and disabled
     - ✓ Change date to refresh booking list

4. **Reservations Page**: http://127.0.0.1:8000/reservations/
   - Displays all bookings as JSON data

5. **API Endpoint**: http://127.0.0.1:8000/bookings/
   - Returns all bookings as JSON
   - With date parameter: http://127.0.0.1:8000/bookings/?date=2024-12-13

6. **Admin Panel**: http://127.0.0.1:8000/admin/
   - Login with superuser credentials
   - View and manage bookings

## API Endpoints

### GET /bookings/
- Returns all bookings as JSON
- Optional query parameter: `?date=YYYY-MM-DD` to filter by date

**Example Response:**
```json
[
  {
    "id": 1,
    "first_name": "John",
    "reservation_date": "2024-12-13",
    "reservation_slot": 18
  }
]
```

### POST /bookings/
- Creates a new booking
- Request body (JSON):
```json
{
  "first_name": "John",
  "reservation_date": "2024-12-13",
  "reservation_slot": 18
}
```

## Database Model

### Booking Model

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key (auto-generated) |
| first_name | CharField(max_length=200) | Customer's first name |
| reservation_date | DateField | Date of reservation |
| reservation_slot | SmallIntegerField | Hour of reservation (10-20) |

**Constraints:**
- `unique_together`: ('reservation_date', 'reservation_slot') - Prevents duplicate bookings

## Technologies Used

- **Backend**: Django 4.x
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS with Fetch API)
- **Dependency Management**: Pipenv

## Grading Checklist

Use this checklist when reviewing:

- [ ] Restaurant app is in INSTALLED_APPS (settings.py)
- [ ] MySQL database is configured (settings.py)
- [ ] Migrations have been performed successfully
- [ ] Booking form has three fields: First name, Reservation date, Reservation slot
- [ ] Date selector opens when clicking reservation date field
- [ ] All bookings displayed as JSON on /reservations/ page
- [ ] Duplicate booking prevented (database constraint)
- [ ] Changing date refreshes booking data
- [ ] Booked time slots are disabled/grey in dropdown
- [ ] API endpoint supports date filtering (/bookings/?date=YYYY-MM-DD)
- [ ] "No Booking" message shown when no reservations for selected date
- [ ] Fetch API used for data retrieval
- [ ] Current date automatically selected on page load

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Ensure MySQL server is running
   - Verify database credentials in settings.py
   - Check if 'littlelemon' database exists

2. **ModuleNotFoundError: No module named 'MySQLdb'**
   - Install mysqlclient: `pipenv install mysqlclient`
   - On Windows, you might need: `pip install mysqlclient`

3. **Static files not loading**
   - Run: `python manage.py collectstatic`
   - Ensure DEBUG=True in settings.py for development

4. **Port already in use**
   - Use a different port: `python manage.py runserver 8001`

## Notes for Reviewers

- The MySQL username and password in settings.py are set to common defaults (`root`/`password`)
- Please update these credentials to match your local MySQL setup before running migrations
- The application uses pipenv for dependency management as required
- All required features from the grading criteria have been implemented
- The booking form prevents duplicate bookings both at the database level (unique constraint) and UI level (disabled slots)

## Author

Created for the Meta Back-End Developer Capstone Project
