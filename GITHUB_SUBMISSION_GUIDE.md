# Little Lemon API - GitHub Submission Guide

## 📋 Project Overview

This is the **Django REST Framework Capstone Project** for the Little Lemon Restaurant API.

### ✅ All Required Features Implemented:

1. ✅ **Django serves static HTML content** - Home, About, and Booking pages
2. ✅ **Project committed to Git repository** - All code tracked and versioned
3. ✅ **Backend connects to MySQL database** - Configured in settings.py
4. ✅ **Menu API implemented** - Full CRUD (GET, POST, PUT, PATCH, DELETE)
5. ✅ **Table Booking API implemented** - Full CRUD operations
6. ✅ **User registration and authentication** - Token-based auth with Djoser
7. ✅ **Unit tests included** - Comprehensive test coverage
8. ✅ **API testable with Insomnia** - Collection file included

---

## 🚀 How to Push to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click the **+** icon → **New repository**
3. Name it: `littlelemon-api` or `django-rest-capstone`
4. **DO NOT** initialize with README (we already have one)
5. Click **Create repository**

### Step 2: Push Your Code

GitHub will show you commands. Use these:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload

- Visit your repository on GitHub
- You should see all 33 files
- Verify **README.txt** is visible on the main page

---

## 📤 Submitting for Peer Review

### In the Course Platform:

1. Click **"My submission"** tab
2. **Project Title**: `Django REST Framework - Little Lemon API Capstone`
3. **GitHub URL**: Paste your repository URL
   - Example: `https://github.com/yourusername/littlelemon-api`
4. Click **"Preview"** to verify
5. Click **"Submit"**

---

## 🧪 What Peer Reviewers Will See

When reviewers clone your repository, they'll find:

### 📁 Key Files for Review:

- **README.txt** ⭐ - Complete API documentation with all endpoints
- **Pipfile** - All dependencies listed
- **manage.py** - Django management script
- **littlelemon/settings.py** - MySQL config, REST Framework config
- **restaurant/models.py** - Menu and Booking models
- **restaurant/serializers.py** - DRF serializers
- **restaurant/views.py** - ViewSets with CRUD operations
- **restaurant/tests.py** - Comprehensive unit tests
- **Insomnia_Collection.json** - Pre-configured API tests

### 🔍 Reviewers Will Test:

1. **Clone your repo**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Setup and run**:
   ```bash
   pipenv install
   python manage.py migrate
   python manage.py runserver
   ```

3. **Test with Insomnia**:
   - Import `Insomnia_Collection.json`
   - Register user
   - Get auth token
   - Test Menu and Booking APIs

4. **Run tests**:
   ```bash
   python manage.py test restaurant
   ```

---

## 📊 API Endpoints Summary (for README.txt)

**Authentication:**
- `POST /auth/users/` - Register
- `POST /auth/token/login/` - Login (get token)

**Menu API (requires auth):**
- `GET /api/menu/` - List all
- `POST /api/menu/` - Create
- `GET /api/menu/{id}/` - Get one
- `PUT /api/menu/{id}/` - Update
- `PATCH /api/menu/{id}/` - Partial update
- `DELETE /api/menu/{id}/` - Delete

**Booking API (requires auth):**
- `GET /api/bookings/` - List all
- `POST /api/bookings/` - Create
- `GET /api/bookings/{id}/` - Get one
- `PUT /api/bookings/{id}/` - Update
- `PATCH /api/bookings/{id}/` - Partial update
- `DELETE /api/bookings/{id}/` - Delete

---

## ✨ Project Highlights

### Technology Stack:
- Django 4.x
- Django REST Framework
- MySQL Database
- Djoser (Authentication)
- Token Authentication
- Comprehensive Unit Tests

### API Features:
- RESTful design
- Token-based authentication
- Full CRUD operations
- Pagination support
- Input validation
- Error handling

### Code Quality:
- Clean, documented code
- Separation of concerns
- DRF best practices
- Comprehensive test coverage
- Git version control

---

## 🎯 Grading Criteria Checklist

| Criteria | Status | Location |
|----------|--------|----------|
| Django serves HTML | ✅ | `/`, `/about/`, `/book/` |
| Git repository | ✅ | Initial commit with all files |
| MySQL connection | ✅ | `littlelemon/settings.py` |
| Menu API | ✅ | `restaurant/views.py` - MenuViewSet |
| Booking API | ✅ | `restaurant/views.py` - BookingViewSet |
| Authentication | ✅ | Djoser + Token Auth |
| Unit tests | ✅ | `restaurant/tests.py` |
| Insomnia testable | ✅ | `Insomnia_Collection.json` |

---

## 💡 Tips for Peer Reviewers

**If MySQL connection fails:**
- Update credentials in `littlelemon/settings.py`
- Create database: `CREATE DATABASE littlelemon;`

**To quickly test:**
1. Import Insomnia collection
2. Run "Register User" request
3. Run "Login" request → copy token
4. Update `auth_token` environment variable
5. Test all other requests

**To run tests:**
```bash
python manage.py test restaurant
```

All tests should pass! ✅

---

## 📝 Notes

- MySQL credentials default to `root`/`password`
- Reviewers need to update based on their setup
- All API endpoints require authentication except registration and login
- Comprehensive documentation in **README.txt**
- Sample Insomnia collection for easy testing

---

## ✅ Project Status: COMPLETE AND READY FOR SUBMISSION

All requirements met. Code tested. Documentation complete. Ready for peer review!

**Good luck with your submission! 🎉**
