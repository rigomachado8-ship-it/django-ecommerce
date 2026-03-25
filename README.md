# Django eCommerce API Project

## 📌 Overview
This project is a Django-based eCommerce system that provides both:
- Web interface (HTML pages)
- REST API endpoints for stores, products, and reviews

The API allows vendors to create stores, add products, and view related data.

---

## ⚙️ Features Implemented

### ✅ Store Management
- Create store (API + HTML form)
- View vendor stores

### ✅ Product Management
- Add product (API + HTML form)
- View products by store

### ✅ Reviews
- View product reviews via API

---

## 🔗 API Endpoints

| Feature | Method | Endpoint |
|--------|--------|----------|
| Create Store | POST | `/api/store/create/` |
| Add Product | POST | `/api/product/add/` |
| Vendor Stores | GET | `/api/vendor/<vendor_id>/stores/` |
| Store Products | GET | `/api/store/<store_id>/products/` |
| Product Reviews | GET | `/api/products/<product_id>/reviews/` |

---

## 🧪 API Testing

API endpoints were tested using **Thunder Client (VS Code)**.

Each request includes:
- JSON request body (for POST)
- Response output
- Status codes (201 Created)

---

## 📸 Screenshots

All required screenshots are included in the `/screenshots` folder:

- Create Store API
- Add Product API
- Vendor Stores API
- Store Products API
- Product Reviews API
- Create Product Page
- Create Store Page

---

## 🗂 Project Structure

## 🚀 How to Run the Project

1. Clone the repository  
2. Create virtual environment  
3. Install dependencies  
   pip install -r requirements.txt  
4. Run migrations  
   python manage.py migrate  
5. Start server  
   python manage.py runserver  

## 👤 Author
Rodrigo Machado
