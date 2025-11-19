```
# Python User Management API

A simple and powerful User Management System built using FastAPI, SQLite, and SQLAlchemy.

Features:
- User Registration
- User Login (JWT Authentication)
- List Users (Admin Only)
- Search Users
- Filter Users
- View Single User (Role Based Access)

------------------------------------------------------------

TECHNOLOGIES USED
-----------------
- Python 3.12+
- FastAPI
- SQLAlchemy
- SQLite
- Passlib (Password Hashing)
- JWT (python-jose)
- Pydantic v2

------------------------------------------------------------

PROJECT STRUCTURE
-----------------
main.py           → FastAPI main application
auth.py           → JWT creation & login logic
db.py             → Database connection setup
models.py         → SQLAlchemy User Model
schemas.py        → Pydantic models
requirements.txt  → Dependencies
users.db          → SQLite database

------------------------------------------------------------

INSTALLATION & SETUP
--------------------

1. Clone the Project:
   git clone https://github.com/Bhargavghoniya/Python_User_API.git
   cd Python_User_API

2. Create Virtual Environment (optional):
   python -m venv venv

3. Activate Virtual Environment:
   Windows → venv\Scripts\activate.bat
   Linux/Mac → source venv/bin/activate

4. Install Dependencies:
   pip install -r requirements.txt

5. Run Server:
   uvicorn main:app --reload

------------------------------------------------------------

TESTING (Thunder Client / Postman)
----------------------------------

THUNDER CLIENT (VS Code):
- Install Thunder Client extension
- New Request → select GET/POST
- Add URL (example: http://127.0.0.1:8000/register)
- Body → JSON
- For protected endpoints:
  Authorization: Bearer <token>

POSTMAN:
- New Request → GET/POST
- Body → Raw → JSON
- Headers:
  Content-Type: application/json
  Authorization: Bearer <token>

------------------------------------------------------------

API ENDPOINTS
-------------

1. REGISTER USER  
   POST /register  
   Example JSON:
   {
     "name": "Admin User",
     "email": "admin@example.com",
     "password": "admin123",
     "role": "Admin",
     "phone": "9876543210",
     "city": "Rajkot",
     "country": "India"
   }

2. LOGIN USER  
   POST /login  
   {
     "email": "admin@example.com",
     "password": "admin123"
   }

   Response:
   {
     "access_token": "xxxxx.yyyyy.zzzzz",
     "token_type": "bearer"
   }

3. LIST USERS (Admin Only)  
   GET /users  
   Filters:
   /users?q=name/email 
   /users?country=India  
   /users?q=admin&country=India  

4. GET SINGLE USER  
   GET /users/{id}  
   Admin → can view any user  
   Staff → can view only own profile  

------------------------------------------------------------

ALLOWED ROLES
-------------
- Admin
- Staff

------------------------------------------------------------

NOTES
-----
- Passwords securely hashed using Passlib
- JWT authentication required for protected routes
- SQLite DB auto-created
- Clean & modular project structure

------------------------------------------------------------

AUTHOR
------
Bhargav Ghoniya
GitHub: https://github.com/Bhargavghoniya
```
