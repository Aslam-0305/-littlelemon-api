from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create router for viewsets
router = DefaultRouter()
router.register(r'menu', views.MenuViewSet, basename='menu')
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    # Template views
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('book/', views.book, name='book'),
    path('reservations/', views.reservations, name='reservations'),
    
    # Legacy JSON endpoint for booking form
    path('bookings/', views.bookings, name='bookings'),
    
    # REST API endpoints
    path('api/', include(router.urls)),
    path('api/user/', views.user_profile, name='user-profile'),
]
