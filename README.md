# 🚀 Orizzonte Backend API

## 📌 Overview

This project is a **Django REST API** that provides:

* 🔐 Authentication (JWT)
* 👥 Role-Based Access Control (RBAC)
* 👑 Boss / 👨‍💼 Employee / 👤 Client system

The API is designed to be used by a frontend (React / Flutter / etc.).

---

## ⚙️ Tech Stack

* Django
* Django REST Framework
* JWT Authentication (SimpleJWT)
* SQLite (dev)

---

## 🔐 Authentication Flow

### 1. Login

```http
POST /api/token/
```

**Body:**

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

```json
{
  "id": 1,
  "username": "user",
  "email": "user@test.com",
  "role": "boss",
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```

---

### 2. Use Token

Add this header to protected requests:

```
Authorization: Bearer ACCESS_TOKEN
```

---

### 3. Refresh Token

```http
POST /api/token/refresh/
```

```json
{
  "refresh": "REFRESH_TOKEN"
}
```

---

### 4. Logout

```http
POST /api/logout/
```

```json
{
  "refresh": "REFRESH_TOKEN"
}
```

---

## 👥 Roles

| Role     | Permissions                    |
| -------- | ------------------------------ |
| Boss     | Full access (manage employees) |
| Employee | Limited access                 |
| Client   | Basic access                   |

---

## 📡 API Endpoints

---

### 🔓 Public

#### Signup (Client only)

```http
POST /api/signup/
```

```json
{
  "username": "client1",
  "email": "client@test.com",
  "password": "test123456"
}
```

---

### 🔐 Authenticated

#### Get Current User

```http
GET /api/users/me/
```

**Response:**

```json
{
  "id": 1,
  "username": "user",
  "email": "user@test.com",
  "role": "client",
  "date_joined": "..."
}
```

---

## 👑 Boss Only Endpoints

mn9drch npuchi data base , tsema bh tkhdem boss wla admin account :
Create boss account manually:

1. python manage.py createsuperuser   

2. Go to admin panel   

3. Set role = Boss         

 // ida mfhmtch roh l chat chof kifeh dir run ll projet mb3d mdlo hed les ettapes li rani ketebhm y3tik les commandes exate li ts7a9hm bh tkhdm admin .

 }  

### Create Employee

```http
POST /api/users/employees/
```

```json
{
  "username": "emp1",
  "password": "test123456",
  "email": "emp@test.com"
}
```

---

### List Employees

```http
GET /api/users/employees/
```

---

### Get Employee Details

```http
GET /api/users/employees/<id>/
```

---

### Delete Employee

```http
DELETE /api/users/employees/<id>/
```

---

## 🚨 Security Rules

* ❌ Clients cannot access employee endpoints
* ❌ Employees cannot manage other employees
* ✔ Only Boss can manage employees
* ✔ Roles are assigned by backend (cannot be faked)

---

## 🧪 Testing

Recommended tool: **Postman**

### Test Flow:

1. Signup (client)
2. Login
3. Copy access token
4. Test `/me`
5. Test employee endpoints
6. Logout

---

## ⚠️ Common Errors

| Error            | Meaning                  |
| ---------------- | ------------------------ |
| 401 Unauthorized | Missing or invalid token |
| 403 Forbidden    | Not allowed (wrong role) |
| 400 Bad Request  | Invalid data             |

---

## 🧠 Notes for Frontend Developers

* Always store:

  * `access`
  * `refresh`
  * `role`
* Use `role` for routing (dashboard)
* Refresh token when access expires
* Handle 401 by redirecting to login

---

## 🏁 Status

✔ Authentication implemented
✔ Role-based access control working
✔ Employee management complete
✔ API tested and stable

---

## 👨‍💻 Author

Backend developed for Orizzonte project.
------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------


# Missions App — Integration Guide

## Overview

The `missions` app implements the full moving-order lifecycle:

```
Client estimates price → Client confirms → Mission created (pending)
                                               ↓
                                    Employee accepts (atomic)
                                               ↓
                                         Mission accepted
                                               ↓
                                        Mission completed
```

---

## 1. Prerequisites

Your project must already have:
- Django REST Framework installed and configured
- SimpleJWT (or equivalent) for authentication
- A `User` model with a `role` field that returns `"client"`, `"employee"`, or `"boss"`

If your role system uses groups or another mechanism, update `missions/permissions.py` accordingly.

---

## 2. Installation

### 2.1 Add to `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    ...
    "missions",
]
```

### 2.2 Include URLs

```python
# project/urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path("api/", include("missions.urls")),
]
```

### 2.3 Run Migrations

```bash
python manage.py makemigrations missions
python manage.py migrate
```

---

## 3. API Reference

All endpoints require a valid JWT in the `Authorization: Bearer <token>` header.

### Client Endpoints

#### `POST /api/missions/estimate/`
Returns a price estimate. **No mission is created.**

**Request body:**
```json
{
  "truck_type": "medium",
  "category": "closed",
  "capacity": 5,
  "departure_latitude": "36.737232",
  "departure_longitude": "3.086472",
  "arrival_latitude": "36.365000",
  "arrival_longitude": "6.614000",
  "distance": "300.00",
  "date": "2024-08-01",
  "time": "09:00:00",
  "workers": 2
}
```

**Response `200 OK`:**
```json
{
  "estimated_price": "65000.00",
  "breakdown": {
    "distance_km": "300.00",
    "workers": 2,
    "price_per_km": 200,
    "fixed_fuel_cost": 2000,
    "price_per_worker": 1500
  }
}
```

---

#### `POST /api/missions/confirm/`
Confirms the mission. **Creates the Mission in the database.**
Accepts the same body as `/estimate/`. Price is always recalculated server-side.

**Response `201 Created`:**
```json
{
  "id": 42,
  "truck_type": "medium",
  "category": "closed",
  "capacity": 5,
  "departure_latitude": "36.737232",
  "departure_longitude": "3.086472",
  "arrival_latitude": "36.365000",
  "arrival_longitude": "6.614000",
  "distance": "300.00",
  "date": "2024-08-01",
  "time": "09:00:00",
  "workers": 2,
  "price": "65000.00",
  "status": "pending",
  "created_at": "2024-07-15T10:00:00Z"
}
```

---

### Employee Endpoints

#### `GET /api/missions/available/`
Returns all non-completed missions with frontend colour-coding fields.

**Response `200 OK`:**
```json
[
  {
    "id": 42,
    "status": "pending",
    "is_taken": false,
    "taken_by": null,
    ...
  },
  {
    "id": 41,
    "status": "accepted",
    "is_taken": true,
    "taken_by": "Ali Boumediene",
    ...
  }
]
```

Frontend logic:
- `is_taken: false` → show card in **green**
- `is_taken: true` → show card in **red** with label `"Taken by: {taken_by}"`

---

#### `POST /api/missions/<id>/accept/`
Atomically assigns the employee to the mission.

**Response `200 OK`** — updated mission with `status: "accepted"`.

**Response `409 Conflict`** — if another employee already accepted it:
```json
{ "detail": "Mission #42 has already been accepted by emp1." }
```

---

### Boss Endpoints

#### `GET /api/missions/all/`
Returns all missions with full detail.

Optional query parameter: `?status=pending|accepted|completed`

**Response `200 OK`:**
```json
[
  {
    "id": 42,
    "client": { "id": 1, "username": "client1", "full_name": "Youcef Benali" },
    "assigned_employee": { "id": 3, "username": "emp1", "full_name": "Ali Boumediene" },
    "price": "65000.00",
    "status": "accepted",
    ...
  }
]
```

---

## 4. Architecture

```
missions/
├── models.py          # DB structure only — Mission model
├── serializers.py     # Validation + serialization only
├── views.py           # Thin API endpoints — delegate to services
├── services.py        # ALL business logic (pricing, creation, acceptance)
├── permissions.py     # Role-based DRF permission classes
├── urls.py            # URL patterns
├── admin.py           # Django admin
└── tests/
    ├── test_services.py   # Unit tests for business logic
    └── test_views.py      # Integration tests for API endpoints
```

**Rule:** Views must never contain business logic. If it's not validation or HTTP response handling, it belongs in `services.py`.

---

## 5. Concurrency Safety

Mission acceptance uses `SELECT FOR UPDATE` inside an atomic transaction:

```python
with transaction.atomic():
    mission = Mission.objects.select_for_update().get(pk=mission_id)
    if mission.status != MissionStatus.PENDING:
        raise MissionAlreadyAcceptedError(...)
    mission.status = MissionStatus.ACCEPTED
    mission.assigned_employee = employee
    mission.save()
```

This guarantees that even if two employees click "Accept" simultaneously, only one succeeds. The database row lock prevents concurrent writes.

**Requirement:** This requires a database that supports row-level locking (PostgreSQL recommended).

---

## 6. Pricing Formula

```
price = (distance_km × 200) + 2000 + (workers × 1500)
```

Constants are defined in `services.py`:
```python
PRICE_PER_KM    = Decimal("200")
FIXED_FUEL_COST = Decimal("2000")
PRICE_PER_WORKER = Decimal("1500")
```

To change pricing, update only these constants.

---

## 7. Running Tests

```bash
pytest missions/tests/ -v
```

Requires `pytest-django`. Add to `pytest.ini`:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = your_project.settings
```

---

## 8. Extending

### Adding a new role
1. Add a permission class in `permissions.py`
2. Use it in the relevant view's `permission_classes`

### Adding mission completion (employee marks done)
1. Add `complete_mission(mission_id, employee)` to `services.py`
2. Add `CompleteMissionView` to `views.py`
3. Add URL to `urls.py`

### Adding notifications
Hook into `services.py` — add notification calls after state changes without touching views or models.
------------------------------------------------------------------------------------------
POST /missions/<id>/start/ -----> in_progress
POST /missions/<id>/complete/
------------------------------------------------------------------------------------------
last part 


### Boss Dashboard API

A single endpoint that returns all key business metrics for the current period.
Designed to power an analytics dashboard — one request gives the boss a complete operational picture without further querying.
### Endpoint
GET /api/missions/dashboard/

Authentication
All requests must include a valid JWT Bearer Token in the Authorization header.

Role required: boss
Requests from client or employee accounts will be rejected with 403 Forbidden.


Request
No request body is required. The endpoint accepts only GET requests.
Headers
GET /api/missions/dashboard/ HTTP/1.1
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

Response
Status
CodeMeaning200 OKStatistics returned successfully401 UnauthorizedMissing or invalid JWT token403 ForbiddenAuthenticated user is not a boss
Body
json{
  "total_missions_month": 40,
  "completed_missions": 25,
  "completion_percentage": 62.5,
  "today_missions": 5,
  "monthly_revenue": "150000.00",
  "monthly_overview": [
    { "month": "November", "year": 2024, "completed": 8  },
    { "month": "December", "year": 2024, "completed": 14 },
    { "month": "January",  "year": 2025, "completed": 12 },
    { "month": "February", "year": 2025, "completed": 18 },
    { "month": "March",    "year": 2025, "completed": 25 },
    { "month": "April",    "year": 2025, "completed": 7  }
  ]
}

Response Fields
Top-level metrics
FieldTypeDescriptiontotal_missions_monthintegerTotal number of missions created since the first day of the current calendar month. Includes all statuses: pending, accepted, in_progress, and completed.completed_missionsintegerNumber of missions that reached completed status within the current calendar month.completion_percentagefloatPercentage of this month's missions that are completed. Rounded to two decimal places. Returns 0.0 when total_missions_month is zero.today_missionsintegerNumber of missions created today (based on the server's local date). Includes all statuses.monthly_revenuedecimalSum of the price field for all completed missions in the current calendar month, in DZD. Returns "0.00" when there are no completed missions.monthly_overviewarrayCompleted mission counts for each of the last 6 calendar months, ordered oldest to newest. Always contains exactly 6 entries. See Monthly Overview below.
Monthly Overview
Each object in the monthly_overview array represents one calendar month:
FieldTypeDescriptionmonthstringFull English month name (e.g. "January", "February").yearintegerFour-digit calendar year (e.g. 2025). Included so entries remain unambiguous when the 6-month window crosses a year boundary.completedintegerNumber of missions that reached completed status during that month. Returns 0 for months with no completed missions — entries are never omitted.

Business Rules
Completion Percentage
Calculated as:
completion_percentage = (completed_missions / total_missions_month) × 100

Rounded to 2 decimal places.
Returns 0.0 if there are no missions this month, avoiding division by zero.

Revenue Calculation
monthly_revenue counts only completed missions. Missions in pending, accepted, or in_progress status do not contribute to revenue, regardless of their price.
monthly_revenue = SUM(price) WHERE status = "completed"
                              AND created_at >= first day of current month
Monthly Overview Window

Always covers exactly 6 months: the current month and the 5 months immediately before it.
Entries are ordered chronologically (oldest first, current month last).
Months with zero completed missions still appear in the list with "completed": 0.
The year field correctly handles the window crossing a calendar year boundary (e.g. November 2024 → April 2025).


Edge Cases
ScenarioBehaviourNo missions created this monthAll counters are 0, percentage is 0.0, revenue is "0.00"Missions exist but none are completedcompleted_missions: 0, completion_percentage: 0.0, monthly_revenue: "0.00"A month in the overview has no completed missionsEntry still appears with "completed": 0Window spans two calendar yearsyear field disambiguates entries (e.g. "month": "December", "year": 2024)

Example: Empty Month
When no missions have been created yet:
json{
  "total_missions_month": 0,
  "completed_missions": 0,
  "completion_percentage": 0.0,
  "today_missions": 0,
  "monthly_revenue": "0.00",
  "monthly_overview": [
    { "month": "November", "year": 2024, "completed": 0 },
    { "month": "December", "year": 2024, "completed": 0 },
    { "month": "January",  "year": 2025, "completed": 0 },
    { "month": "February", "year": 2025, "completed": 0 },
    { "month": "March",    "year": 2025, "completed": 0 },
    { "month": "April",    "year": 2025, "completed": 0 }
  ]
}