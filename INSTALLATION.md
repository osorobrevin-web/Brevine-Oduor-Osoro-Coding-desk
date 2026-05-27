# TICKETZETU Flask Application - Installation Guide

## Quick Setup Instructions

### Step 1: Create Directory Structure
```bash
mkdir app\core app\auth app\admin app\client app\customer app\templates app\templates\auth app\templates\admin app\templates\client app\templates\customer app\templates\components
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Create All Python Modules

The application requires the following file structure:

```
ticketzetu-flask/
├── run.py                      # Entry point
├── config.py                   # ✓ Already created
├── requirements.txt            # ✓ Already created
├── setup_dirs.py              # ✓ Already created
│
├── app/
│   ├── __init__.py            # See APP_INIT_PY.txt
│   ├── models.py              # ✓ Already created
│   ├── decorators.py          # ✓ Already created
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── utils.py           # ✓ Already created
│   │
│   ├── auth/
│   │   ├── __init__.py        # Entry point for auth blueprint
│   │   ├── routes.py          # See AUTH_ROUTES_PY.txt
│   │   └── forms.py           # ✓ Already created
│   │
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── routes.py          # See ADMIN_ROUTES_PY.txt
│   │   └── forms.py
│   │
│   ├── client/
│   │   ├── __init__.py
│   │   ├── routes.py          # See CLIENT_ROUTES_PY.txt
│   │   └── forms.py
│   │
│   ├── customer/
│   │   ├── __init__.py
│   │   ├── routes.py          # See CUSTOMER_ROUTES_PY.txt
│   │   └── forms.py
│   │
│   └── templates/
│       ├── base.html
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
│       │   └── commissions.html
│       ├── customer/
│       │   ├── dashboard.html
│       │   ├── browse_events.html
│       │   ├── purchases.html
│       │   └── reviews.html
│       └── components/
│           ├── navbar.html
│           ├── sidebar.html
│           └── footer.html
```

### Step 4: Manual File Creation

Since you cannot use PowerShell directly, follow these steps:

1. **Open Command Prompt (cmd.exe)**
2. **Navigate to project directory:**
   ```
   cd "c:\Users\User\Documents\Brevine Osoro Coding Desk.worktrees\agents-ticket-system-structure-admin-client"
   ```

3. **Create directories:**
   ```
   mkdir app\core app\auth app\admin app\client app\customer
   mkdir app\templates app\templates\auth app\templates\admin app\templates\client app\templates\customer app\templates\components
   ```

4. **Create empty __init__.py files:**
   ```
   type nul > app\__init__.py
   type nul > app\core\__init__.py
   type nul > app\auth\__init__.py
   type nul > app\admin\__init__.py
   type nul > app\client\__init__.py
   type nul > app\customer\__init__.py
   ```

5. **Copy file contents from .txt files to actual .py files:**
   - Copy APP_INIT_PY.txt content to app/__init__.py
   - Copy APP_MODELS_PY.txt content to app/models.py
   - etc.

### Step 5: Run the Application
```bash
python run.py
```

Then open http://localhost:5000 in your browser.

---

## File Contents Reference

See the accompanying .txt files for code:
- `APP_INIT_PY.txt` → `app/__init__.py`
- `APP_MODELS_PY.txt` → `app/models.py`
- `ADMIN_ROUTES_PY.txt` → `app/admin/routes.py`
- And others...

## Features Implemented

✅ **Role-Based Authentication**
- Admin: System management
- Client: Event/ticket creation
- Customer: Browse and purchase tickets

✅ **Complete Separation**
- Each role sees only their dashboard
- Protected routes with decorators
- No feature bleed between roles

✅ **SQLite Database**
- Clean relational schema
- User roles: Admin, Client, Customer
- Event, Ticket, Review, Payout tracking

✅ **Bootstrap UI**
- Responsive templates
- Professional styling
- Mobile-friendly

## Next Steps

After running the application:

1. **Register a test account** - Choose a role (Admin/Client/Customer)
2. **Log in** - Verify role-specific dashboard
3. **Test features** - Try features specific to each role

## Admin Credentials (Optional)

To seed admin account, add to `run.py` after creating app:
```python
with app.app_context():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(id=generate_id(), username='admin', email='admin@ticketzetu.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
```
