# 📦 Orders Manager Service

A lightweight, modern, and high-performance asynchronous Flask web application for internal order management and product catalog control.
Built with a clean architecture approach, featuring asynchronous dependency injection and robust authentication.

## 🚀 Features

* **Asynchronous Core:** Leverages Flask 2.0+ async capabilities combined with `Uvicorn` for optimal performance.
* **Dependency Injection:** Powered by **Dishka** for clean, scoped, and robust object-graph management.
* **Data Validation:** Strict and reliable request validation via **Pydantic v2**, including custom phone and email sanitizers.
* **Secure Authentication:** Built-in Admin panel protection using **Flask-Login** seamlessly bridged into the async pipeline.
* **Dynamic Order Builder:** Advanced form parsing logic that maps flat HTML checkbox forms directly into structured nested Pydantic data schemas.
* **User-Friendly UI:** Responsive administration templates styled with **Bootstrap 5**, native icons, and client-side input masking (`IMask`).

---

## 🛠️ Tech Stack

* **Backend Framework:** Flask (Async mode)
* **Dependency Injection:** Dishka
* **Validation & Serialization:** Pydantic v2
* **Authentication:** Flask-Login & Werkzeug Security
* **Frontend UI:** Jinja2 templates, Bootstrap 5, Bootstrap Icons, IMask.js
* **Containerization:** Docker & Docker Compose

---

## 🚦 Quick Start

Prerequisites
Docker and Docker Compose installed.

### 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DollaR84/order_service.git
   cd order_service
   ```

2. Environment Setup
   Copy the `.env.example` file to `.env` and configure your settings:
   ```bash
   cp .env.example .env
   ```

3. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```
   
4. **For test and develop:**
   ```bash
   pip install pytest pytest-asyncio aiosqlite
   ```

### 🧪 Running Tests

   ```bash
   pytest backend/ -v
   ```

### 🐳 Running with Docker

   You can also run **Order Service** itself inside a container:
   ```bash
   docker compose build
   docker compose up -d
   ```
