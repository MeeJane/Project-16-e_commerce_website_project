# 🛒 BuddyBasket – Django E-Commerce Website

BuddyBasket is a full-featured e-commerce web application built with **Django**. It provides a seamless online shopping experience with secure authentication, product browsing, cart management, order placement, and integrated online payments using Razorpay.

## 🚀 Live Demo

**Website:** https://jafawais0330.pythonanywhere.com/

## 📌 Features

* User registration and authentication
* Product listing with categories
* Wishlist functionality for saving favorite products.
* Product search options.
* Product detail pages
* Shopping cart management
* Checkout process
* Razorpay payment gateway integration
* Order placement and confirmation
* Responsive user interface
* Admin panel for product and order management
* Media and static file handling

## 🛠️ Tech Stack

* Python
* Django
* SQLite
* HTML5
* CSS3
* JavaScript
* Razorpay API

## 📂 Project Structure

```text
E_Commerce_BuddyBasket_Project/
├── buddybasket/
├── E_Commerce_BuddyBasket_Project/
├── media/
├── static/
├── manage.py
├── requirements.txt
└── db.sqlite3
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/MeeJane/Project-16-e_commerce_website_project.git
```

Navigate to the project:

```bash
cd Project-16-e_commerce_website_project/E_Commerce_BuddyBasket_Project
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## 💳 Payment Integration

BuddyBasket integrates the **Razorpay Payment Gateway** for secure online transactions. Configure your Razorpay API keys as environment variables before enabling payments.

## 📸 Key Modules

* Home Page
* Product Catalog
* Category Management
* Product Details
* Shopping Cart
* Checkout
* Payment Gateway
* Order Management
* User Authentication
* Django Admin Dashboard

## 📦 Deployment

The application is deployed on **PythonAnywhere** and configured with:

* Static file collection
* Media file handling
* Environment variables
* SQLite database
* Production-ready Django configuration


## 🚀 Future Enhancements


* Product search with advanced filtering and sorting options.
* Product reviews and ratings by verified customers.
* User profile management with order history and saved addresses.
* Email notifications for registration, orders, and shipping updates.
* Coupon codes, discounts, and promotional offers.
* Inventory and stock management with low-stock alerts.
* Multiple payment gateway support (Stripe, PayPal, UPI, etc.).
* Order tracking with shipment status updates.
* Product recommendation system based on user preferences.
* AI-powered product search and chatbot assistance.
* Multi-vendor marketplace support.
* Responsive Progressive Web App (PWA) for mobile users.
* Admin analytics dashboard with sales and customer insights.
* Multi-language and multi-currency support for global users.
* REST API integration for mobile applications.
* Social login (Google, GitHub, Facebook) for faster authentication.


## 📄 License

This project is intended for educational, learning, and portfolio purposes.
