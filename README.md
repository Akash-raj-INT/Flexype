# 🛒 Smart Inventory Reservation System

A backend-focused Django project that prevents inventory overselling during high-traffic scenarios such as flash sales by using **time-based inventory reservations**, **JWT authentication**, and **transactional concurrency control**.

---

## 📌 Problem Statement

In e-commerce platforms, multiple users may attempt to purchase the same product simultaneously.  
This often leads to:
- Overselling of inventory
- Inventory locked by abandoned carts
- Unfair checkout experience

This project solves these issues by introducing a **temporary reservation system** with expiry.

---

## 🚀 Features

- Inventory is **never oversold**
- Time-based inventory reservation (5-minute expiry)
- Inventory auto-released on expiry or cancellation
- JWT-based authentication (User & Admin)
- Concurrency-safe using database transactions
- Idempotent APIs
- Clean layered backend architecture

---

## 🧱 Architecture

API Layer (Views)
↓
Service Layer (Business Logic)
↓
Data Layer (Models / Database)


- **Models** → Inventory, Reservation, User
- **Services** → Reservation & checkout logic
- **Views** → REST APIs
- **Auth** → JWT (SimpleJWT)

---

## 🛠️ Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: SQLite
- **Concurrency Control**: `@transaction.atomic`, `select_for_update`
- **Testing Tool**: Thunder Client / Postman

---

## 🔐 Authentication

- Users authenticate using **JWT tokens**
- Admin manages inventory via Django Admin
- Protected APIs require:
Authorization: Bearer <ACCESS_TOKEN>


---

## 📡 API Endpoints

### 1️⃣ Reserve Inventory


POST /inventory/reserve

Reserves inventory temporarily when user starts checkout.

**Request**
```json
{
  "sku": "IPHONE15"
}


Response

{
  "reservation_id": "UUID",
  "expires_at": "timestamp"
}

2️⃣ Confirm Checkout
POST /checkout/confirm


Finalizes purchase after payment success.

Request

{
  "reservation_id": "UUID"
}

3️⃣ Cancel Checkout
POST /checkout/cancel


Releases reserved inventory if user cancels.

4️⃣ Inventory Status
GET /inventory/{sku}


Returns real-time stock availability.

Response

{
  "sku": "IPHONE15",
  "total_stock": 5,
  "available_stock": 4
}
