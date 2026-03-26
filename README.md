# Django eCommerce Project (Part 1)

## 📌 Overview

This project is a Django-based eCommerce application that allows vendors to create and manage stores and products. It includes REST API endpoints for handling stores, products, and reviews, along with frontend pages for user interaction.

---

## 🚀 Features

### 🏪 Store Management

* Create stores via API and UI
* View stores by vendor

### 📦 Product Management

* Add products to stores
* View products for each store
* Product detail page

### 🧑‍💼 Vendor Features

* Vendor dashboard
* Vendor store list page
* Vendor product list page

### ⭐ Reviews

* Product reviews API endpoint

### 🌐 External Integration

* Reddit feed page displaying external data

---

## 🔌 API Endpoints

| Endpoint                     | Method | Description               |
| ---------------------------- | ------ | ------------------------- |
| `/api/store/create/`         | POST   | Create a new store        |
| `/api/product/add/`          | POST   | Add a new product         |
| `/api/vendor/<id>/stores/`   | GET    | Get stores for a vendor   |
| `/api/store/<id>/products/`  | GET    | Get products for a store  |
| `/api/product/<id>/reviews/` | GET    | Get reviews for a product |

---

## 🛠️ Technologies Used

* Python
* Django
* Django REST Framework
* SQLite
* HTML (Django Templates)
* Thunder Client (API testing)

---

## 📂 Project Structure

django_ecommerce_part1/
│
├── ecommerce_project/
├── store/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│
├── screenshots/
├── manage.py
├── requirements.txt
└── README.md

---

## 📸 Screenshots

All required screenshots are located in the `/screenshots/` folder:

* create_store_api.png
* create_product_api.png
* vendor_stores_api.png
* store_products_api.png
* product_reviews_api.png
* reddit_feed.png
* vendor_dashboard.png
* vendor_stores_page.png
* vendor_products_page.png
* product_detail.png

---

## ▶️ How to Run the Project

1. Clone the repository:
   git clone https://github.com/rigomachado8-ship-it/django_ecommerce_part1.git

2. Navigate into the project:
   cd django_ecommerce_part1

3. Create a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Apply migrations:
   python manage.py migrate

6. Run the development server:
   python manage.py runserver

7. Open in browser:
   http://127.0.0.1:8000/

---

## ✅ Notes

* APIs were tested using Thunder Client
* Screenshots are included as proof of functionality
* Project follows Django best practices

---

## 👨‍💻 Author

Rodrigo Machado
