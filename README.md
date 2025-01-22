# Library Service Project

"""
This project aims to automate the operations of a local library by introducing an online management system.
"""

## Features

### Book Management

- CRUD Functionality: Add, update, delete, and list books.

- Inventory Management: Track the number of available books in the library.

- Book Details: Includes title, author, cover type (HARD/SOFT), inventory count, and daily fee (in USD).

### User Management

- Authentication & Registration: Secure user registration and login using JWT tokens.

- User Roles: Support for regular users and staff (admin) roles.

- Profile Management: View and update user profiles.

### Borrowing Management

- Borrow Books: Users can borrow books if inventory is available.

- Return Books: Track the actual return date and update book inventory.

- Borrowing History: Filter borrowings by user and status (active or returned).

### Payment Processing (Stripe Integration)

- Payment Types: Handle payments for borrowing fees and fines.

- Stripe Integration: Secure payment sessions using Stripe.

- Payment Status: Track payment status (PENDING/PAID).

- Session Details: Includes Stripe session URL and ID.

## API Endpoints

### Books Service

- POST /books/ - Add a new book.

- GET /books/ - Get a list of books.

- GET /books/<id>/ - Get details of a specific book.

- PUT/PATCH /books/<id>/ - Update book details, including inventory.

- DELETE /books/<id>/ - Delete a book.

### Users Service

- POST /users/ - Register a new user.

- POST /users/token/ - Obtain JWT tokens.

- POST /users/token/refresh/ - Refresh JWT tokens.

- GET /users/me/ - Get user profile information.

- PUT/PATCH /users/me/ - Update user profile.

### Borrowings Service

- POST /borrowings/ - Create a new borrowing (decreases book inventory by 1).

- GET /borrowings/?user_id=...&is_active=... - Filter borrowings by user ID and active status.

- GET /borrowings/<id>/ - Get details of a specific borrowing.

- POST /borrowings/<id>/return/ - Mark borrowing as returned (increases book inventory by 1).

### Payments Service

- GET /payments/success/ - Confirm successful payment.

- GET /payments/cancel/ - Handle canceled payments.

## Implementation Details

### Books Service

- Permissions: Only admin users can create, update, or delete books. All users can view book lists and details.

- Authentication: Uses JWT tokens for secure access.

### Users Service

- Custom User Model: Includes email-based authentication.

- ModHeader Compatibility: Supports Authorize header for JWT authentication.

### Borrowings Service

- Constraints: Ensures valid borrow and return dates.

- Filtering: Supports filtering by user ID and active borrowings.

- Return Validation: Prevents duplicate returns.

### Payments Service

- Stripe Integration: Uses the stripe package for payment processing.

- Test Environment: Operates in Stripe's test mode (no real money involved).

- Admin Access: Admins can view all payments, while users can view only their own.
