# TICKETZETU Flask - Complete Setup Guide

## 🚀 Overview

Your TICKETZETU Flask application is a **role-based ticketing system** with three completely separated dashboards:
- **Admin Dashboard** - System management and reporting
- **Client Dashboard** - Event and ticket creation
- **Customer Dashboard** - Browse and purchase tickets

## 📁 Generated Files

All necessary Python files have been created. Files with `.txt` extension contain code that needs to be saved as `.py` files.

### Already Created ✓
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `app/models.py` - Database models
- `app/decorators.py` - Access control
- `app/core/utils.py` - Shared utilities
- `app/auth/forms.py` - Authentication forms
- `run.py` - Flask entry point

### Code in .txt Files (Copy to .py)
- `APP_INIT_PY.txt` → `app/__init__.py`
- `AUTH_ROUTES_PY.txt` → `app/auth/routes.py`
- `ADMIN_ROUTES_PY.txt` → `app/admin/routes.py`
- `CLIENT_ROUTES_PY.txt` → `app/client/routes.py`
- `CUSTOMER_ROUTES_PY.txt` → `app/customer/routes.py`
- `BASE_HTML.txt` → `app/templates/base.html`

## 🔧 Setup Steps

### Step 1: Create Directory Structure

**Using Command Prompt (cmd.exe):**

```batch
cd "c:\Users\User\Documents\Brevine Osoro Coding Desk.worktrees\agents-ticket-system-structure-admin-client"

mkdir app\core
mkdir app\auth
mkdir app\admin
mkdir app\client
mkdir app\customer
mkdir app\templates\auth
mkdir app\templates\admin
mkdir app\templates\client
mkdir app\templates\customer
mkdir app\templates\components
```

**Or manually:** Create these folders in the project directory using File Explorer.

### Step 2: Create __init__.py Files

Create empty files named `__init__.py` in these directories (right-click → New → Text Document, then rename):
- `app\__init__.py`
- `app\core\__init__.py`
- `app\auth\__init__.py`
- `app\admin\__init__.py`
- `app\client\__init__.py`
- `app\customer\__init__.py`

### Step 3: Copy Code from .txt Files

For each `.txt` file listed above:

1. Open the `.txt` file
2. Select all content (Ctrl+A)
3. Copy (Ctrl+C)
4. Create the corresponding `.py` file in the same directory
5. Paste the content (Ctrl+V)
6. Save

**Example for APP_INIT_PY.txt:**
- Open `APP_INIT_PY.txt`
- Copy all content
- Create `app\__init__.py`
- Paste content
- Save

### Step 4: Install Dependencies

Open Command Prompt in the project directory:

```bash
pip install -r requirements.txt
```

This installs:
- Flask 2.3.2
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.2
- Flask-WTF 1.1.1
- WTForms 3.0.1
- Email-validator 2.0.0
- Werkzeug 2.3.6

### Step 5: Create Additional Templates

You need minimal HTML templates to get started. For now, create these empty templates:

```
app/templates/auth/login.html
app/templates/auth/register.html
app/templates/auth/unauthorized.html
app/templates/admin/dashboard.html
app/templates/admin/users.html
app/templates/admin/events.html
app/templates/admin/tickets.html
app/templates/admin/payouts.html
app/templates/admin/reports.html
app/templates/client/dashboard.html
app/templates/client/events.html
app/templates/client/create_event.html
app/templates/client/manage_tickets.html
app/templates/client/event_detail.html
app/templates/client/commissions.html
app/templates/customer/dashboard.html
app/templates/customer/browse_events.html
app/templates/customer/event_detail.html
app/templates/customer/purchases.html
app/templates/customer/review_event.html
app/templates/customer/my_reviews.html
```

For now, each can just contain:
```html
{% extends "base.html" %}
{% block content %}
<h1>{{ title }}</h1>
<p>Content coming soon...</p>
{% endblock %}
```

### Step 6: Run the Application

```bash
python run.py
```

You'll see output like:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### Step 7: Open in Browser

Navigate to: **http://localhost:5000**

## 🔐 First Run - Create Test Accounts

1. Click "Register"
2. Create test accounts:
   - **Admin User**: username=`admin`, role=`Admin - Manage System`
   - **Client User**: username=`client`, role=`Client - Sell Tickets`
   - **Customer User**: username=`customer`, role=`Customer - Buy Tickets`

3. Log in with each account and verify you see the correct dashboard

## 📊 Features by Role

### Admin Dashboard
- View all users
- Manage events and tickets
- Process payouts
- Generate reports
- View system statistics

### Client Dashboard
- Create events
- Add tickets to events
- Track commissions
- View revenue details
- Manage event listings

### Customer Dashboard
- Browse available events
- Purchase tickets
- Write reviews
- View purchase history
- Track spending

## 🗄️ Database

The application uses **SQLite** with these tables:
- `users` - User accounts (Admin/Client/Customer)
- `events` - Events created by clients
- `tickets` - Ticket listings and purchases
- `cancellations` - Cancelled tickets
- `customers` - Customer profiles
- `reviews` - Event reviews
- `payouts` - Client payouts
- `admins` - Admin profiles

Database file location: `ticketzetu.db` (auto-created)

## 🎨 Styling

Templates use **Bootstrap 5** with custom styling for:
- Navigation bar
- Sidebar navigation (role-specific)
- Dashboard cards
- Responsive design
- Dark blue/green color scheme

## 🔒 Security

✅ **Role-Based Access Control (RBAC)**
- Decorators enforce role restrictions
- Users only see their role's dashboard
- Routes reject unauthorized access

✅ **Password Security**
- Passwords hashed with Werkzeug
- Login validation
- Session management with Flask-Login

✅ **Form Validation**
- CSRF protection with Flask-WTF
- Email validation
- Required field validation

## 📝 Environment Variables (Optional)

Create a `.env` file for production:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///ticketzetu.db
```

## ❌ Troubleshooting

**Error: ModuleNotFoundError**
- Ensure all __init__.py files exist in each package
- Run `pip install -r requirements.txt` again

**Error: Database locked**
- Close Flask app and check for multiple instances
- Delete `ticketzetu.db` to reset database

**Templates not rendering**
- Verify template filenames match exactly
- Check template directory structure

**Login/Register not working**
- Ensure forms.py has been created in app/auth/
- Check that models.py exists in app/

## 📞 Support

For questions about the ticketing system logic, refer to the original files in `projects/` folder.

## 🎯 Next Steps

1. ✓ Follow setup steps above
2. ✓ Create test accounts
3. ✓ Verify all three dashboards work
4. Create full HTML templates for each page
5. Add event images/media
6. Implement email notifications
7. Add payment processing
8. Deploy to production

---

**TICKETZETU** - Powered by BReSCA  
Brevine e-Systems Consultancy Agency, Kisumu Kenya
