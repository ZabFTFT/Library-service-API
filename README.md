# Library Management System
This is a library management system built with Django that allows users to browse books, borrow books, and make payments for overdue books.

# Features
- **Book Service**: CRUD functionality for books, with permissions allowing only admin users to create/update/delete books.
- **User Service**: CRUD functionality for users with JWT authentication.
- **Borrowing Service**: Allows users to borrow books, with validation to ensure that book inventory is not 0. Decreases book inventory by 1 for each successful borrowing. Non-admin users can only see their own borrowings, while admin users can view all users' borrowings.
- **Payment Service**: Allows users to make payments for overdue books, with Stripe payment integration. Fine payments are also included for overdue books.
# Getting Started
1. Clone the repository.
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Set up your environment variables by creating a `.env` file based on the `.env.sample` file.
4. Set up your database by running python manage.py migrate.
5. Start the development server by running python manage.py runserver.
# Usage
## Books Service
- **GET /books**: List all books.
- **POST /books**: Create a new book (admin only).
- **GET /books/{book_id}**: Retrieve details for a specific book.
- **PUT /books/{book_id}**: Update details for a specific book (admin only).
- **DELETE /books/{book_id}**: Delete a specific book (admin only).
## User Service
- **GET /users**: List all users.
- **POST /users**: Create a new user.
- **GET /users/{user_id}**: Retrieve details for a specific user.
- **PUT /users/{user_id}**: Update details for a specific user.
- **DELETE /users/{user_id}**: Delete a specific user.
## Borrowing Service
- **GET /borrowings**: List all borrowings for the current user.
- **GET /borrowings?is_active=true**: List all active borrowings for the current user.
- **GET /borrowings?is_active=false**: List all returned borrowings for the current user.
- **GET /borrowings?user_id={user_id}**: List all borrowings for a specific user (admin only).
- **GET /borrowings/{borrowing_id}**: Retrieve details for a specific borrowing.
- **POST /borrowings**: Create a new borrowing.
- **PUT /borrowings/{borrowing_id}**: Return a specific borrowing.
- **GET /borrowings/{borrowing_id}/fine_payment**: Retrieve details for a specific fine payment.
## Payment Service
- **GET /payments**: List all payments for the current user.
- **GET /payments/{payment_id}**: Retrieve details for a specific payment.
- **POST /payments**: Create a new payment session.
## Notifications
Notifications are sent to a Telegram chat whenever a new borrowing is created or a borrowing becomes overdue.

## Credits
This project was created by Vlad Zabolotnyi (Team lead), Ostap Turianskyi, Oleksandr Zhukov, Mykhailo Vovchok, Artur Tytomyr.
