# 🎫 TICKETZETU Flask - Quick Start

## What Was Created

Your Flask ticketing system has been set up with a **modular, role-based architecture**:

### ✅ Core Files (Already Created)
- `config.py` - Flask configuration
- `requirements.txt` - Python dependencies
- `run.py` - Flask entry point
- `app/models.py` - Database models
- `app/decorators.py` - Access control
- `app/core/utils.py` - Shared utilities  
- `app/auth/forms.py` - Authentication forms
- `auto_setup.py` - **Automatic setup script** ⚡

### 📝 Code Files (Need setup)
- Separate `.txt` files contain code for `.py` files
- `auto_setup.py` can automatically copy all of them

### 📊 Architecture

```
TICKETZETU (Single Flask App)
  ├── Admin Dashboard (Full system control)
  ├── Client Dashboard (Event/ticket management)
  └── Customer Dashboard (Purchase tickets)

✨ Complete Separation: No feature bleed between roles
```

## ⚡ Fast Setup (Recommended)

### Option A: Automatic Setup (Easiest)

```bash
# Run this single command:
python auto_setup.py
```

This script will:
1. Create all directories
2. Create all __init__.py files
3. Copy code from .txt files to .py files
4. Generate template files
5. Show you the next steps

### Option B: Manual Setup (10 minutes)

See **SETUP_GUIDE.md** for detailed step-by-step instructions.

## 🚀 After Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python run.py

# 3. Open browser
# http://localhost:5000
```

## 📋 Test the System

After running:

1. **Register** three test accounts:
   - Username: `admin`, Role: Admin
   - Username: `client`, Role: Client  
   - Username: `customer`, Role: Customer

2. **Log in** with each and verify:
   - Different dashboards appear
   - Different navigation menus
   - No feature bleed

## 🔑 Key Features

✅ **Role-Based Access Control (RBAC)**
- Decorators protect routes
- Users only see their role's features
- Invalid access redirects to unauthorized page

✅ **SQLite Database**
- Lightweight, file-based
- Automatic schema creation
- Relations between users, events, tickets

✅ **Bootstrap Styling**
- Responsive design
- Dark professional theme
- Mobile-friendly

✅ **Complete Separation**
- Admin cannot see customer features
- Client cannot see admin controls
- Customer cannot access ticket creation

## 📁 File Structure Created

```
ticketzetu-flask/
├── run.py                              (Entry point)
├── config.py                           (Flask config) ✓
├── requirements.txt                    (Dependencies) ✓
├── auto_setup.py                       (Setup script) ✓
├── SETUP_GUIDE.md                      (Manual setup)
├── INSTALLATION.md                     (Details)
│
├── app/
│   ├── __init__.py                     (Flask factory)
│   ├── models.py                       (Database) ✓
│   ├── decorators.py                   (RBAC) ✓
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── utils.py                    (Helpers) ✓
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py                   (Login/Register)
│   │   └── forms.py                    (Forms) ✓
│   │
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── routes.py                   (Admin routes)
│   │   └── forms.py
│   │
│   ├── client/
│   │   ├── __init__.py
│   │   ├── routes.py                   (Client routes)
│   │   └── forms.py
│   │
│   ├── customer/
│   │   ├── __init__.py
│   │   ├── routes.py                   (Customer routes)
│   │   └── forms.py
│   │
│   └── templates/
│       ├── base.html                   (Main layout)
│       ├── auth/
│       │   ├── login.html
│       │   ├── register.html
│       │   └── unauthorized.html
│       ├── admin/
│       │   ├── dashboard.html
│       │   ├── users.html
│       │   ├── events.html
│       │   ├── tickets.html
│       │   ├── payouts.html
│       │   └── reports.html
│       ├── client/
│       │   ├── dashboard.html
│       │   ├── events.html
│       │   ├── create_event.html
│       │   ├── manage_tickets.html
│       │   ├── event_detail.html
│       │   └── commissions.html
│       └── customer/
│           ├── dashboard.html
│           ├── browse_events.html
│           ├── event_detail.html
│           ├── purchases.html
│           ├── review_event.html
│           └── my_reviews.html
│
└── ticketzetu.db                       (Database, auto-created)
```

## 🎯 Admin Dashboard Features

- View all users
- Manage events
- View all tickets
- Process payouts
- Generate system reports

## 🎯 Client Dashboard Features

- Create events
- Add tickets to events
- Track commissions
- View revenue analytics

## 🎯 Customer Dashboard Features

- Browse events
- Purchase tickets
- Leave reviews
- View purchase history

## ❓ FAQ

**Q: Can I merge the three dashboards into one file?**  
A: Yes! They're already in `app/__init__.py` which loads all three blueprints.

**Q: How do I prevent admins from seeing customer pages?**  
A: Use the `@admin_required`, `@client_required`, or `@customer_required` decorators.

**Q: How do I add a new feature to the client dashboard?**  
A: Add a route in `app/client/routes.py` and a template in `app/templates/client/`.

**Q: Is the database secure?**  
A: Passwords are hashed with Werkzeug. Use HTTPS in production.

---

**Ready to go?** Run `python auto_setup.py` now! 🚀
