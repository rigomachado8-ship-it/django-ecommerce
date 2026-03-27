# Django eCommerce Project (Part 1)

## Overview

This project is a Django-based eCommerce web application that allows users to register as buyers or vendors. Vendors can create stores and manage products, while buyers can browse products, add them to a cart, and place orders.

The system also includes REST API endpoints, authentication, and password reset functionality.

---

## Technologies Used

* Python 3
* Django
* Django REST Framework
* MySQL
* HTML (Django Templates)
* Bootstrap 5

---

## Features

### User Management

* User registration with role selection (buyer/vendor)
* Login and logout functionality
* Role-based dashboards

### Vendor Features

* Create, update, and delete stores
* Add, update, and delete products
* View products by store

### Buyer Features

* Browse products
* Add products to cart
* Checkout and place orders
* View order history

### Additional Features

* Product reviews
* Password reset via email
* Reddit feed integration
* REST API endpoints for stores, products, and reviews

---

## Project Structure

```
store/
├── models.py
├── views.py
├── serializers.py
├── forms.py
├── templates/
│   └── store/
│       ├── base.html
│       ├── home.html
│       └── ...
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rigomachado8-ship-it/django_ecommerce_part1.git
cd django_ecommerce_part1
```

---

## Database Setup (MySQL) ⚠️ IMPORTANT

### 1. Start MySQL

```bash
mysql -u root -p
```

Enter your MySQL password.

---

### 2. Create the database

```sql
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### 3. (Optional but Recommended) Create a dedicated user

```sql
CREATE USER 'ecom_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecom_user'@'localhost';
FLUSH PRIVILEGES;
```

---

### 4. Configure Django database settings

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_db',
        'USER': 'root',  # or 'ecom_user'
        'PASSWORD': 'YOUR_PASSWORD',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

---

## Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 3. Create superuser

```bash
python manage.py createsuperuser
```

---

### 4. Run development server

```bash
python manage.py runserver
```

---

### 5. Access the application

* Home: http://127.0.0.1:8000/
* Admin: http://127.0.0.1:8000/admin/

---

## API Endpoints

| Endpoint                     | Method   | Description       |
| ---------------------------- | -------- | ----------------- |
| `/api/product/list/`         | GET      | List all products |
| `/api/product/<id>/`         | GET      | Product details   |
| `/api/product/create/`       | POST     | Create product    |
| `/api/store/create/`         | POST     | Create store      |
| `/api/store/<id>/products/`  | GET      | Store products    |
| `/api/vendor/<id>/stores/`   | GET      | Vendor stores     |
| `/api/product/<id>/reviews/` | GET/POST | Product reviews   |

---

## Design Considerations

* Models are designed with proper relationships (Store → Product → Order)
* Validation ensures data integrity (e.g., store must have description and address)
* Role-based access control for buyers and vendors
* Clean separation of concerns using forms, serializers, and views

---

## Code Quality

* Docstrings follow PEP 257 conventions
* Clear and modular structure
* Reusable components across views, forms, and templates

---

## Author

Rodrigo Machado

---

## Notes

* Ensure MySQL is running before starting the Django server
* Database must be created before running migrations
* Use a virtual environment for dependency management
