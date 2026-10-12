document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('booking-form');
    const dateInput = document.getElementById('reservation_date');
    const slotSelect = document.getElementById('reservation_slot');
    const bookingsList = document.getElementById('bookings-list');
    const messageDiv = document.getElementById('message');

    // Set current date as default
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
    dateInput.setAttribute('min', today);

    // Load bookings for current date on page load
    loadBookings(today);

    // Listen for date changes
    dateInput.addEventListener('change', function() {
        const selectedDate = this.value;
        loadBookings(selectedDate);
        messageDiv.style.display = 'none';
    });

    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const firstName = document.getElementById('first_name').value;
        const reservationDate = dateInput.value;
        const reservationSlot = slotSelect.value;

        if (!firstName || !reservationDate || !reservationSlot) {
            showMessage('Please fill in all fields', 'error');
            return;
        }

        // Create booking
        fetch('/bookings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                first_name: firstName,
                reservation_date: reservationDate,
                reservation_slot: parseInt(reservationSlot)
            })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => Promise.reject(err));
            }
            return response.json();
        })
        .then(data => {
            showMessage('Booking successful!', 'success');
            form.reset();
            dateInput.value = reservationDate; // Keep the same date
            loadBookings(reservationDate);
        })
        .catch(error => {
            if (error.error) {
                showMessage(error.error, 'error');
            } else {
                showMessage('Failed to create booking. Please try again.', 'error');
            }
        });
    });

    // Function to load bookings for a specific date
    function loadBookings(date) {
        fetch(`/bookings/?date=${date}`)
            .then(response => response.json())
            .then(bookings => {
                displayBookings(bookings, date);
                updateAvailableSlots(bookings);
            })
            .catch(error => {
                console.error('Error loading bookings:', error);
                bookingsList.innerHTML = '<p class="error">Failed to load bookings</p>';
            });
    }

    // Function to display bookings
    function displayBookings(bookings, date) {
        if (bookings.length === 0) {
            bookingsList.innerHTML = `<p>No bookings for ${date}</p>`;
            return;
        }

        let html = '<div class="bookings-container">';
        bookings.forEach(booking => {
            html += `
                <div class="booking-item">
                    <strong>${booking.first_name}</strong><br>
                    Time: ${booking.reservation_slot}:00<br>
                    Date: ${booking.reservation_date}
                </div>
            `;
        });
        html += '</div>';
        bookingsList.innerHTML = html;
    }

    // Function to update available slots (disable booked ones)
    function updateAvailableSlots(bookings) {
        const bookedSlots = bookings.map(b => b.reservation_slot);
        const options = slotSelect.querySelectorAll('option');
        
        options.forEach(option => {
            if (option.value === '') return; // Skip the placeholder option
            
            const slotValue = parseInt(option.value);
            if (bookedSlots.includes(slotValue)) {
                option.disabled = true;
                option.style.backgroundColor = '#f0f0f0';
                option.style.color = '#999';
                option.textContent = option.textContent.split(' -')[0] + ' - Booked';
            } else {
                option.disabled = false;
                option.style.backgroundColor = '';
                option.style.color = '';
                option.textContent = option.textContent.split(' -')[0];
            }
        });
    }

    // Function to show messages
    function showMessage(message, type) {
        messageDiv.textContent = message;
        messageDiv.className = 'message ' + type;
        messageDiv.style.display = 'block';
        
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
});
