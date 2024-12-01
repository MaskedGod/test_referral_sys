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
