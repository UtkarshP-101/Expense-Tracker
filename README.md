## 🧾 Expense Tracker (Flask + JWT)

A simple **Expense Tracker web application** built using **Flask**, **JWT authentication**, and **SQLite**.  
Users can register, log in securely, and manage their personal expenses (add, edit, delete).

---

## 🚀 Features

- 🔐 User authentication using **JWT (JSON Web Tokens)**
- 📝 Register & Login with hashed passwords
- 📊 Add, edit, and delete expenses
- 👤 User-specific dashboard
- 🍪 JWT stored securely in HTTP-only cookies
- 💾 SQLite database
- 🎨 Clean UI with HTML, CSS, and Bootstrap

---

## 🛠 Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy  
- **Authentication:** JWT (PyJWT)  
- **Database:** SQLite  
- **Frontend:** HTML, CSS, Bootstrap  
- **Password Hashing:** Werkzeug  

---

## 📂 Project Structure
```
expense-tracker/
│
├── app.py
├── auth.py
├── dashboard.py
├── extensions.py
├── expenses.db
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── add_expense.html
│ └── edit_expense.html
│
├── static/
│ ├── register.css
│ └── login.css
│
├── requirements.txt
└── README.md
```


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

### 2️⃣ Create a virtual environment
```
python -m venv venv
```
Activate it:
  Windows
  ```
  venv\Scripts\activate
  ```
  MacOS
  ```
  source venv/bin/activate
  ```

### 3️⃣ Install dependencies
```
pip install flask flask-sqlalchemy pyjwt werkzeug
```

### 4️⃣ Run the application
```
python app.py
```

---
## 🔑 Authentication Flow
1. User logs in using email & password
2. Server verifies credentials
3. A JWT token is created
4. Token is stored in an HTTP-only cookie
5. Protected routes verify the token before allowing access

---
## 🧠 Security Notes
- Passwords are never stored in plain text
- JWT tokens automatically expire
- Cookies are HTTP-only to prevent JavaScript access
- Users can only access their own expenses

---
## 🙌 Learning Outcome

- This project helped me learn:
- Flask app structuring using Blueprints
- JWT-based authentication
- Secure password handling
- Database relationships
- Jinja templating
- Frontend & backend integration

## Working


https://github.com/user-attachments/assets/3af22f83-d1b6-4235-abbe-85dcf3bcfb19









