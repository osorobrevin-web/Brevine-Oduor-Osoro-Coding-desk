# 📚 TICKETZETU Flask - Complete Documentation Index

## 🎯 Start Here

**New to this project?** Read in this order:
1. **README_FLASK.md** ← START HERE (Quick overview)
2. **SETUP_GUIDE.md** ← Setup instructions
3. **INSTALLATION.md** ← Detailed setup reference

## 📁 What Was Created

### Configuration Files ✅
- **config.py** - Flask configuration, database setup
- **requirements.txt** - All Python dependencies
- **run.py** - Application entry point (runs the Flask app)

### Python Core ✅  
- **app/models.py** - Database models (User, Event, Ticket, etc.)
- **app/decorators.py** - Role-based access control (@admin_required, @client_required, @customer_required)
- **app/core/utils.py** - Shared utilities (commission calculations, ID generation)
- **app/auth/forms.py** - Login and registration forms

### Automatically Generated Code
The following files contain code that needs to be extracted:

| File | Purpose |
|------|---------|
| APP_INIT_PY.txt | `app/__init__.py` - Flask factory & app setup |
| AUTH_ROUTES_PY.txt | `app/auth/routes.py` - Login, register, logout |
| ADMIN_ROUTES_PY.txt | `app/admin/routes.py` - Admin dashboard & management |
| CLIENT_ROUTES_PY.txt | `app/client/routes.py` - Event & ticket management |
| CUSTOMER_ROUTES_PY.txt | `app/customer/routes.py` - Event browsing & purchasing |
| BASE_HTML.txt | `app/templates/base.html` - Main layout template |

### Setup Scripts
- **auto_setup.py** - Automatic setup (Recommended!)
- **setup_dirs.py** - Manual directory creation

### Documentation
- **README_FLASK.md** - Quick start guide
- **SETUP_GUIDE.md** - Step-by-step setup
- **INSTALLATION.md** - Detailed installation
- **DOCUMENTATION.md** - This file

## 🚀 Quick Start

### Fastest Way (1 command)
```bash
python auto_setup.py
```

This does:
1. Creates all directories
2. Copies code from .txt files to .py files
3. Generates template files
4. Shows next steps

### Then Run:
```bash
pip install -r requirements.txt
python run.py
```

Open: http://localhost:5000

## 🏗️ Architecture

### System Design
```
┌─────────────────────────────────────────┐
│         TICKETZETU Flask App            │
├─────────────────────────────────────────┤
│                                         │
│  Authentication (app/auth/)             │
│  ├─ Login/Register with roles           │
│  └─ Protected by @login_required        │
│                                         │
│  Role-Based Routing                     │
│  ├─ Admin (@admin_required)             │
│  ├─ Client (@client_required)           │
│  └─ Customer (@customer_required)       │
│                                         │
│  Database (SQLite)                      │
│  ├─ Users (with roles)                  │
│  ├─ Events (created by clients)         │
│  ├─ Tickets (managed by system)         │
│  ├─ Payouts (for clients)               │
│  ├─ Reviews (by customers)              │
│  └─ Cancellations (tracked)             │
│                                         │
│  Web Interface (Bootstrap)               │
│  ├─ Admin Dashboard                     │
│  ├─ Client Dashboard                    │
│  └─ Customer Dashboard                  │
└─────────────────────────────────────────┘
```

### Role Separation

| Feature | Admin | Client | Customer |
|---------|-------|--------|----------|
| **Dashboard** | System overview | Event management | Ticket purchasing |
| **Users** | Manage all users | Personal profile | Personal profile |
| **Events** | View all | Create & manage own | Browse & filter |
| **Tickets** | Manage all | Create batches | Purchase & track |
| **Payouts** | Process & track | View earnings | N/A |
| **Reviews** | View reports | N/A | Write & read |
| **Reports** | Generate system reports | Commission tracking | Purchase history |

## 🗄️ Database Schema

### Users Table
```sql
- id (UUID)
- username (unique)
- email (unique)
- password_hash
- phone
- role (admin/client/customer)
- is_active
- created_at
```

### Events Table
```sql
- id (UUID)
- client_id (FK → users)
- name
- description
- date
- location
- capacity
- created_at
```

### Tickets Table
```sql
- id (UUID)
- event_id (FK → events)
- client_id (FK → users)
- customer_id (FK → users, nullable)
- price
- bresca_commission
- mpesa_cost
- status (available/sold/cancelled)
- purchased_at
```

### Other Tables
- **Cancellations** - Refund tracking
- **Reviews** - Customer event reviews
- **Payouts** - Client earnings
- **Customer** - Customer profile info
- **Admin** - Admin profile info

## 🔐 Access Control

### Decorators in app/decorators.py

```python
@admin_required         # Only admins
@client_required        # Only clients
@customer_required      # Only customers
```

Routes without decorators require `@login_required` only.

### Example:
```python
@app.route('/admin/users')
@login_required
@admin_required
def manage_users():
    # Only authenticated admins can access
```

## 📊 Commission Rules

From **app/core/utils.py**:

| Price Range | Commission |
|-------------|-----------|
| $0 | $0 |
| ≤ 500 | 50 |
| ≤ 2000 | 8% |
| ≤ 5000 | 7% |
| > 5000 | 6% |

Plus: 10 KES M-Pesa transaction cost per ticket

## 🎨 UI/Styling

- **Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Color Scheme**: Dark blue/green professional theme
- **Layout**: Responsive with sidebar navigation
- **Mobile**: Fully mobile-friendly

## 🔧 Configuration

### Environment Variables (Optional)
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///ticketzetu.db
```

### Default Settings
- Database: SQLite (ticketzetu.db)
- Debug Mode: Enabled (in development)
- Secret Key: Auto-generated (change in production)
- Session Timeout: 24 hours

## 📝 File Organization

```
Project Root/
├── Application Files
│   ├── run.py                    Entry point
│   ├── config.py                 Configuration
│   ├── requirements.txt           Dependencies
│   └── auto_setup.py             Setup automation
│
├── Flask App (app/)
│   ├── __init__.py               App factory
│   ├── models.py                 Database models
│   ├── decorators.py             Access control
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── utils.py              Utilities
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py             Auth routes
│   │   └── forms.py              Auth forms
│   │
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── routes.py             Admin routes
│   │   └── forms.py              Admin forms
│   │
│   ├── client/
│   │   ├── __init__.py
│   │   ├── routes.py             Client routes
│   │   └── forms.py              Client forms
│   │
│   ├── customer/
│   │   ├── __init__.py
│   │   ├── routes.py             Customer routes
│   │   └── forms.py              Customer forms
│   │
│   └── templates/
│       ├── base.html             Main layout
│       ├── auth/                 Auth templates
│       ├── admin/                Admin templates
│       ├── client/               Client templates
│       └── customer/             Customer templates
│
├── Database
│   └── ticketzetu.db             SQLite database (auto-created)
│
└── Documentation
    ├── README_FLASK.md           Quick start
    ├── SETUP_GUIDE.md            Setup instructions
    ├── INSTALLATION.md           Detailed installation
    └── DOCUMENTATION.md          This file
```

## 🧪 Testing the Application

### 1. Register Test Accounts
```
Account 1: admin/admin123 (role: Admin)
Account 2: client/client123 (role: Client)
Account 3: customer/customer123 (role: Customer)
```

### 2. Verify Role Separation
- Login as admin → see admin dashboard
- Login as client → see client dashboard
- Login as customer → see customer dashboard

### 3. Test Access Control
- Try accessing `/admin/...` as customer → should redirect
- Try accessing `/client/...` as admin → should redirect

## 🚨 Common Issues & Solutions

### ModuleNotFoundError
**Problem**: Cannot find app module
**Solution**: Ensure all `__init__.py` files exist in each package

### TemplateNotFound
**Problem**: HTML templates not loading
**Solution**: Verify template filenames in `app/templates/` directory

### Database Locked
**Problem**: Database file is locked
**Solution**: Close all Flask instances and restart

### Import Errors
**Problem**: Circular imports or missing modules
**Solution**: Run `pip install -r requirements.txt` again

## 🌐 URL Routes

### Auth Routes
- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/logout` - Logout
- `/auth/unauthorized` - Access denied page

### Admin Routes
- `/admin/dashboard` - Admin overview
- `/admin/users` - User management
- `/admin/events` - Event management
- `/admin/tickets` - Ticket management
- `/admin/payouts` - Payout management
- `/admin/reports` - System reports

### Client Routes
- `/client/dashboard` - Client overview
- `/client/events` - My events
- `/client/event/create` - Create new event
- `/client/event/<id>/tickets` - Manage tickets
- `/client/commissions` - Commission tracking

### Customer Routes
- `/customer/dashboard` - Customer overview
- `/customer/browse` - Browse events
- `/customer/event/<id>` - Event details
- `/customer/event/<id>/buy` - Purchase ticket
- `/customer/purchases` - My purchases
- `/customer/event/<id>/review` - Leave review
- `/customer/reviews` - My reviews

## 💡 Tips & Best Practices

1. **Always validate input** on routes
2. **Use decorators** consistently for access control
3. **Test with multiple roles** to verify separation
4. **Keep business logic** in utils.py
5. **Use templates** for consistent UI
6. **Backup database** before major changes
7. **Use environment variables** in production

## 🔄 Development Workflow

1. Make changes to routes or models
2. Flask auto-reloads (debug mode enabled)
3. Test in browser or with curl
4. Commit changes to Git

## 📖 Additional Resources

- Flask: https://flask.palletsprojects.com/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/
- Bootstrap: https://getbootstrap.com/
- WTForms: https://wtforms.readthedocs.io/

---

**TICKETZETU** - Powered by BReSCA  
Brevine e-Systems Consultancy Agency, Kisumu Kenya

*Last Updated: 2024*
