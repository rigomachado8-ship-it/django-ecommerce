# 🛒 Django E-commerce Project

## 🚀 Live Overview

This is a full-featured e-commerce web application built with Django.
It includes user authentication, product management, cart functionality, checkout flow, and verified purchase reviews.

> ✅ This repository contains a **single, clean Django project** intended for review and demonstration purposes.

---

## 📸 Screenshots

*(Add screenshots here later for extra impact)*

Example:

* Home page
* Product detail page
* Cart page
* Admin dashboard

---

## ✨ Features

### 👤 Authentication

* User registration and login
* Password reset functionality

### 🛍️ Store

* Product listing and detail pages
* Image uploads for products
* Category-based organization (if implemented)

### 🛒 Shopping Experience

* Add/remove items from cart
* Persistent cart behavior
* Checkout flow

### ⭐ Reviews

* Users can leave product reviews
* Reviews restricted to **verified purchasers**

### ⚙️ Admin Panel

* Manage products, users, and orders via Django admin

---

## 🧰 Tech Stack

* **Backend:** Django (Python)
* **Database:** MySQL / SQLite (development)
* **Frontend:** HTML, CSS (Django Templates)
* **Media Handling:** Pillow

---

## ⚡ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rigomachado8-ship-it/django-ecommerce.git
cd django-ecommerce
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create admin user

```bash
python manage.py createsuperuser
```

### 6. Start server

```bash
python manage.py runserver
```

---

## 🌐 Access the App

* Main app: http://127.0.0.1:8000/
* Admin panel: http://127.0.0.1:8000/admin/

---

## 🧪 Demo Account (Optional)

*(Add this later if you want reviewers to log in easily)*

```text
Username: demo
Password: demo123
```

---

## 📂 Project Structure

```text
django-ecommerce/
├── ecommerce_project/   # Main project settings
├── store/               # Core app (products, cart, orders)
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔮 Future Improvements

* 💳 Payment integration (Stripe/PayPal)
* 📦 Order tracking system
* 🌍 Deployment (AWS, Render, or Railway)
* 🎨 Improved UI/UX (React or Tailwind)
* 📊 Analytics dashboard

---

## 🧠 What I Learned

* Building a full-stack Django application
* Structuring scalable Django apps
* Implementing authentication and authorization
* Designing real-world e-commerce logic (cart, checkout, reviews)

---

## 👨‍💻 Author

**Rodrigo Machado**

GitHub: https://github.com/rigomachado8-ship-it
