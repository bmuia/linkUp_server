# LinkUp Backend

LinkUp is a real-time messaging backend built with **Django**, **Django Channels**, and **MongoDB Atlas**.  
It supports **user authentication** and **group messaging**,
---

## Features

- 🔐 **User Authentication** (JWT-based with login, register, logout, and whoami endpoints)  
- 💬 **Group Messaging** (real-time chatroom)

## Tech Stack

- **Backend Framework**: Django + Django REST Framework  
- **WebSockets**: Django Channels + Redis  
- **Database**: MongoDB Atlas  
- **Authentication**: JWT (SimpleJWT)  
- **Deployment**: Render.com  

---

## Installation

### Prerequisites

Make sure you have the following installed:

* **Python** >= 3.12.1
* **pip** (Python package manager)
* **Docker** >= 0.19.0
* **PostgreSQL** (for Django auth & relational data)
* **Redis** (for WebSocket channels & caching)
* **MongoDB** (for storing chat messages)

---

### 1. Clone Repository

```bash
git clone https://github.com/belam-io/linkUp_server.git
cd linkUp_server
```

---

### 2. Setup Environment Variables

Copy the example `.env` file and update the values as needed:

```bash
cp .env.example .env
```

Then edit `.env` with your secrets (DB connection strings, JWT secret, etc.).

---

### 3. Build & Start Containers

```bash
docker compose up -d --build
```

This will spin up all required services (Django app, PostgreSQL, Redis, MongoDB).

---

### 4. (Optional) View Logs

To follow logs in real-time:

```bash
docker compose logs -f
```

---

✅ Once the containers are up, the backend will be available at:
[http://localhost:8000](http://localhost:8000)

For the database ui they are available at:
- [pgadmin](http://localhost:5050)
- [mongoexpress](http://localhost:8081)

# LinkUp Server

Backend service for **LinkUp**, providing user authentication, group chat, and messaging features using Django, Channels, Redis, PostgreSQL, and MongoDB.

## Installation

### Prerequisites

* Python >= 3.12.1
* pip
* Docker >= 0.19.0
* PostgreSQL
* Redis
* MongoDB

### 1. Clone Repository

```bash
git clone https://github.com/belam-io/linkUp_server.git
cd linkUp_server
```

### 2. Setup the .env

Copy the `.env.example` file and update the values accordingly:

```bash
cp .env.example .env
```

### 3. Spin up the containers

```bash
docker compose up -d --build
```

### 4. Optional (for logs)

```bash
docker compose logs -f
```

---

## API Endpoints

### **POST** `/accounts/v1/register/`

* **Request body:**

```json
{
  "email": "string",
  "username": "string",
  "password": "string"
}
```

* **Response:**

```json
{
  "access": "ey...",
  "refresh": "ey..."
}
```

### **POST** `/accounts/v1/login/`

* **Request body:**

```json
{
  "email": "string",
  "password": "string"
}
```

* **Response:**

```json
{
  "access": "ey...",
  "refresh": "ey..."
}
```

### **POST** `/accounts/v1/logout/`

* Requires authentication
* **Request body:**

```json
{
  "refresh": "string"
}
```

* **Response:**
* Status 200–202

### **GET** `/accounts/v1/whoami/`

* Requires authentication
* **Request body:** none
* **Response:**

```json
{
  "id": 1,
  "email": "test@example.com",
  "username": "testuser",
  "first_name": "",
  "last_name": "",
  "profile_pic": null,
  "bio": "",
  "status_message": "",
  "phone_number": null,
  "date_of_birth": null,
  "date_joined": "2025-09-24T16:00:00Z"
}
```

---

## WebSocket Messaging Guide

### Overview

Group messaging is powered by **Django Channels** and **WebSockets**. Unlike REST APIs, WebSockets provide a persistent two-way connection for real-time messaging.

### Authentication

All WebSocket connections must include a valid **JWT access token** in the `Authorization` header.

### Example with wscat

```bash
wscat -c wss://linkup-server.onrender.com/ws/chat/ \
  -H "Authorization: Bearer <your-access-token>"
```

### Sending a message

```json
{
  "message": "Hello from wscat!"
}
```

### Receiving a message

```json
{
  "message": "Hello from wscat!",
  "sender_id": 1,
  "timestamp": "2025-09-24T16:25:01.863928"
}
```

### Message Schema

* **message**: string (the chat text)
* **sender_id**: integer (ID of the sender)
* **timestamp**: ISO 8601 formatted datetime


## Conclusion

This project is still under **active development**. Current functionality includes:

* ✅ User authentication
* ✅ Group chat over WebSockets
* 🚧 Upcoming: one-to-one messaging, message history, privacy controls

We welcome contributions, bug reports, and feature suggestions. Together, we can make LinkUp a reliable real-time communication platform. 💡


