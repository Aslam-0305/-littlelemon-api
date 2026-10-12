from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Booking, Menu
from datetime import datetime
import json
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import MenuSerializer, BookingSerializer, UserSerializer
from django.contrib.auth.models import User


# Template views (for serving HTML)
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    return render(request, 'book.html')


def reservations(request):
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'reservations.html', {'bookings': booking_json})


# Legacy JSON endpoint (for the booking form)
def bookings(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        if date:
            bookings = Booking.objects.filter(reservation_date=date)
        else:
            bookings = Booking.objects.all()
        
        booking_list = []
        for booking in bookings:
            booking_list.append({
                'id': booking.id,
                'first_name': booking.first_name,
                'reservation_date': str(booking.reservation_date),
                'reservation_slot': booking.reservation_slot
            })
        
        return JsonResponse(booking_list, safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            reservation_date = data.get('reservation_date')
            reservation_slot = data.get('reservation_slot')
            
            # Check if booking already exists
            if Booking.objects.filter(reservation_date=reservation_date, reservation_slot=reservation_slot).exists():
                return JsonResponse({'error': 'Slot already booked'}, status=400)
            
            booking = Booking.objects.create(
                first_name=first_name,
                reservation_date=reservation_date,
                reservation_slot=reservation_slot
            )
            
            return JsonResponse({
                'id': booking.id,
                'first_name': booking.first_name,
                'reservation_date': str(booking.reservation_date),
                'reservation_slot': booking.reservation_slot
            }, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# REST API ViewSets
class MenuViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Menu items.
    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Bookings/Table Reservations.
    Supports: GET (list/detail), POST, PUT, PATCH, DELETE
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


# Additional API views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
