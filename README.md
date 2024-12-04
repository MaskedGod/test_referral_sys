# Referral System Implementation with Django

### Test Task for Hammer Systems

## Task Overview

The goal is to implement a simple referral system with a minimal interface for testing. The task involves creating the logic and API for the following features:

### Functional Requirements

- **Phone Number Authentication:**

  - First request: User inputs their phone number. Simulate the sending of a 4-digit verification code (with a server delay of 1-2 seconds).
  - Second request: User inputs the received verification code.
  - If the user has not previously authenticated, record them in the database.

- **User Profile:**

  - On first authentication, assign the user a randomly generated 6-character invite code (comprising letters and digits).
  - In the profile, allow the user to enter another user's invite code (validate its existence before activation).
  - A user can only activate one invite code. If they have already activated one, it should be displayed in the corresponding field in the profile response.

- **Referral Tracking:**

  - The API should return a list of phone numbers for users who have entered the current user's invite code.

- **API Implementation:**

  - Develop and document APIs for all the above functionality.

- **Testing Setup:**

  - Provide a Postman collection with all relevant requests.

- **Deployment:**
  - Host the project online for easier testing.

### Optional Features

- Interface development using Django Templates.
- API documentation with ReDoc.
- Docker support.

### Technology Stack Requirements

- **Programming Language:** Python
- **Framework:** Django, Django REST Framework (DRF)
- **Database:** PostgreSQL
- Other tools and libraries are up to your discretion.

# Referral System Implementation with Django

This project is a referral system implementation for **Hammer Systems**. It includes phone number authentication, user profiles with invite codes, referral tracking, and an API built using Django and Django REST Framework (DRF). The system is also documented using Swagger and ReDoc.

## Features

### 1. Phone Number Authentication

- Users can authenticate via their phone number. A 4-digit verification code is sent and validated for login.

### 2. User Profile

- Each user is assigned a 6-character invite code upon first authentication.
- Users can input another user's invite code, which can only be activated once.

### 3. Referral Tracking

- Users can see the phone numbers of individuals who used their invite code for registration.

### 4. API Documentation

- The APIs are documented with Swagger and ReDoc for easy testing and understanding.

## Technology Stack

- **Backend Framework:** Django 5.1, Django REST Framework
- **Database:** PostgreSQL
- **API Documentation:** Swagger, ReDoc
- **Caching:** Django's cache framework (for handling verification codes)

## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MaskedGod/test_referral_sys.git
   cd referral-system
   ```

2. **Set up a virtual environment and install dependencies:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure the PostgreSQL database:**
   Update the `DATABASES` settings in `settings.py` with your PostgreSQL credentials.

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Run the server:**

   ```bash
   python manage.py runserver
   ```

6. **API Documentation:**
   - Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
   - ReDoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

## API Endpoints

### Health Check

- **GET** `/health/` - Returns the service status.

### Phone Authentication

- **POST** `/auth/` - Send a verification code to a phone number.

### Verify Code

- **POST** `/verify/` - Verify the received code for a given phone number.

### Profile

- **GET** `/profile/` - Retrieve the user's profile using their phone number.
- **POST** `/profile/` - Activate an invite code for the user.

### Referrals

- **GET** `/referrals/` - Retrieve the list of users who used the current user's invite code.
