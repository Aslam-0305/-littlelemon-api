from django.test import TestCase, Client
from django.urls import reverse
from .models import Booking, Menu
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import date
import json


# Model Tests
class BookingModelTest(TestCase):
    def setUp(self):
        self.booking = Booking.objects.create(
            first_name="John",
            reservation_date="2024-12-13",
            reservation_slot=18
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.first_name, "John")
        self.assertEqual(str(self.booking.reservation_date), "2024-12-13")
        self.assertEqual(self.booking.reservation_slot, 18)

    def test_booking_str(self):
        expected = "John - 2024-12-13 at 18:00"
        self.assertEqual(str(self.booking), expected)

    def test_unique_constraint(self):
        """Test that duplicate bookings for same date/time are not allowed"""
        with self.assertRaises(Exception):
            Booking.objects.create(
                first_name="Jane",
                reservation_date="2024-12-13",
                reservation_slot=18
            )


class MenuModelTest(TestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            title="Greek Salad",
            price=12.99,
            inventory=50
        )

    def test_menu_creation(self):
        self.assertEqual(self.menu_item.title, "Greek Salad")
        self.assertEqual(self.menu_item.price, 12.99)
        self.assertEqual(self.menu_item.inventory, 50)

    def test_menu_str(self):
        expected = "Greek Salad : 12.99"
        self.assertEqual(str(self.menu_item), expected)


# View Tests (Legacy HTML views)
class BookingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.booking = Booking.objects.create(
            first_name="John",
            reservation_date="2024-12-13",
            reservation_slot=18
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_book_page(self):
        response = self.client.get(reverse('book'))
        self.assertEqual(response.status_code, 200)

    def test_reservations_page(self):
        response = self.client.get(reverse('reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

    def test_bookings_api_get_all(self):
        response = self.client.get(reverse('bookings'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['first_name'], 'John')

    def test_bookings_api_get_by_date(self):
        response = self.client.get(reverse('bookings') + '?date=2024-12-13')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_bookings_api_post_success(self):
        data = {
            'first_name': 'Jane',
            'reservation_date': '2024-12-13',
            'reservation_slot': 19
        }
        response = self.client.post(
            reverse('bookings'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 2)


# REST API Tests
class MenuAPITest(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create authentication token
        self.token = Token.objects.create(user=self.user)
        
        # Set up API client with authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create test menu items
        self.menu1 = Menu.objects.create(
            title="Greek Salad",
            price=12.99,
            inventory=50
        )
        self.menu2 = Menu.objects.create(
            title="Pasta",
            price=15.99,
            inventory=30
        )

    def test_get_menu_list(self):
        """Test retrieving list of menu items"""
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_menu_detail(self):
        """Test retrieving a single menu item"""
        response = self.client.get(f'/api/menu/{self.menu1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Greek Salad')
        self.assertEqual(float(response.data['price']), 12.99)

    def test_create_menu_item(self):
        """Test creating a new menu item"""
        data = {
            'title': 'Bruschetta',
            'price': 8.99,
            'inventory': 40
        }
        response = self.client.post('/api/menu/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)
        self.assertEqual(Menu.objects.get(title='Bruschetta').price, 8.99)

    def test_update_menu_item(self):
        """Test updating a menu item (PUT)"""
        data = {
            'title': 'Greek Salad Updated',
            'price': 13.99,
            'inventory': 45
        }
        response = self.client.put(f'/api/menu/{self.menu1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu1.refresh_from_db()
        self.assertEqual(self.menu1.title, 'Greek Salad Updated')
        self.assertEqual(float(self.menu1.price), 13.99)

    def test_partial_update_menu_item(self):
        """Test partially updating a menu item (PATCH)"""
        data = {'price': 14.99}
        response = self.client.patch(f'/api/menu/{self.menu1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu1.refresh_from_db()
        self.assertEqual(float(self.menu1.price), 14.99)
        self.assertEqual(self.menu1.title, 'Greek Salad')  # Unchanged

    def test_delete_menu_item(self):
        """Test deleting a menu item"""
        response = self.client.delete(f'/api/menu/{self.menu1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 1)

    def test_unauthorized_access(self):
        """Test that unauthenticated users cannot access API"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookingAPITest(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create authentication token
        self.token = Token.objects.create(user=self.user)
        
        # Set up API client with authentication
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Create test bookings
        self.booking1 = Booking.objects.create(
            first_name="Alice",
            reservation_date="2024-12-15",
            reservation_slot=12
        )
        self.booking2 = Booking.objects.create(
            first_name="Bob",
            reservation_date="2024-12-15",
            reservation_slot=14
        )

    def test_get_booking_list(self):
        """Test retrieving list of bookings"""
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_booking_detail(self):
        """Test retrieving a single booking"""
        response = self.client.get(f'/api/bookings/{self.booking1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Alice')

    def test_create_booking(self):
        """Test creating a new booking"""
        data = {
            'first_name': 'Charlie',
            'reservation_date': '2024-12-16',
            'reservation_slot': 18
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 3)

    def test_update_booking(self):
        """Test updating a booking (PUT)"""
        data = {
            'first_name': 'Alice Updated',
            'reservation_date': '2024-12-15',
            'reservation_slot': 13
        }
        response = self.client.put(f'/api/bookings/{self.booking1.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking1.refresh_from_db()
        self.assertEqual(self.booking1.first_name, 'Alice Updated')

    def test_delete_booking(self):
        """Test deleting a booking"""
        response = self.client.delete(f'/api/bookings/{self.booking1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 1)

    def test_unauthorized_access(self):
        """Test that unauthenticated users cannot access API"""
        self.client.credentials()  # Remove authentication
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'newuser',
            'password': 'testpass123',
            'email': 'newuser@example.com'
        }

    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post('/auth/users/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')

    def test_token_creation(self):
        """Test token generation on login"""
        # First create a user
        user = User.objects.create_user(**self.user_data)
        
        # Login and get token
        login_data = {
            'username': 'newuser',
            'password': 'testpass123'
        }
        response = self.client.post('/auth/token/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)

    def test_authenticated_request(self):
        """Test making authenticated request with token"""
        # Create user and token
        user = User.objects.create_user(**self.user_data)
        token = Token.objects.create(user=user)
        
        # Make authenticated request
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
