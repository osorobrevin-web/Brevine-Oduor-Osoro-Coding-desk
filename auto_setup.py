#!/usr/bin/env python3
"""
TICKETZETU Flask Setup Script
Automatically sets up the application structure
"""
import os
import shutil
from pathlib import Path

def setup_ticketzetu():
    """Setup TICKETZETU Flask application"""
    
    print("=" * 60)
    print("TICKETZETU Flask Application - Automated Setup")
    print("=" * 60)
    print()
    
    base_path = Path(__file__).parent
    os.chdir(base_path)
    
    # Step 1: Create directories
    print("Step 1: Creating directory structure...")
    directories = [
        'app/core',
        'app/auth',
        'app/admin',
        'app/client',
        'app/customer',
        'app/templates',
        'app/templates/auth',
        'app/templates/admin',
        'app/templates/client',
        'app/templates/customer',
        'app/templates/components',
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {directory}")
    
    print()
    
    # Step 2: Create __init__.py files
    print("Step 2: Creating __init__.py files...")
    init_files = [
        'app/__init__.py',
        'app/core/__init__.py',
        'app/auth/__init__.py',
        'app/admin/__init__.py',
        'app/client/__init__.py',
        'app/customer/__init__.py',
    ]
    
    for init_file in init_files:
        if not Path(init_file).exists():
            Path(init_file).touch()
            print(f"  ✓ Created {init_file}")
        else:
            print(f"  ✓ {init_file} already exists")
    
    print()
    
    # Step 3: Copy code from .txt files to .py files
    print("Step 3: Copying code from .txt files to .py files...")
    file_mappings = {
        'APP_INIT_PY.txt': 'app/__init__.py',
        'AUTH_ROUTES_PY.txt': 'app/auth/routes.py',
        'ADMIN_ROUTES_PY.txt': 'app/admin/routes.py',
        'CLIENT_ROUTES_PY.txt': 'app/client/routes.py',
        'CUSTOMER_ROUTES_PY.txt': 'app/customer/routes.py',
        'BASE_HTML.txt': 'app/templates/base.html',
    }
    
    for src_txt, dest_py in file_mappings.items():
        src_path = Path(src_txt)
        dest_path = Path(dest_py)
        
        if src_path.exists():
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove the "Save as:" comment if present
            if content.startswith('"""'):
                # Find the end of the docstring
                end_idx = content.find('"""', 3)
                if end_idx != -1:
                    content = content[end_idx+3:].lstrip()
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✓ Copied {src_txt} → {dest_py}")
        else:
            print(f"  ✗ {src_txt} not found")
    
    print()
    
    # Step 4: Create template files
    print("Step 4: Creating template files...")
    template_dirs = [
        'app/templates/auth',
        'app/templates/admin',
        'app/templates/client',
        'app/templates/customer',
    ]
    
    base_template = '''{% extends "base.html" %}
{% block title %}{{ page_title }} - TICKETZETU{% endblock %}
{% block content %}
<div class="row">
    <div class="col-12">
        <h1>{{ page_title }}</h1>
        <p class="text-muted">Content for this page is coming soon...</p>
    </div>
</div>
{% endblock %}
'''
    
    template_files = [
        ('app/templates/auth/login.html', 'Login'),
        ('app/templates/auth/register.html', 'Register'),
        ('app/templates/auth/unauthorized.html', 'Unauthorized'),
        ('app/templates/admin/dashboard.html', 'Admin Dashboard'),
        ('app/templates/admin/users.html', 'Manage Users'),
        ('app/templates/admin/events.html', 'All Events'),
        ('app/templates/admin/tickets.html', 'All Tickets'),
        ('app/templates/admin/payouts.html', 'Payouts'),
        ('app/templates/admin/reports.html', 'Reports'),
        ('app/templates/client/dashboard.html', 'Client Dashboard'),
        ('app/templates/client/events.html', 'My Events'),
        ('app/templates/client/create_event.html', 'Create Event'),
        ('app/templates/client/manage_tickets.html', 'Manage Tickets'),
        ('app/templates/client/event_detail.html', 'Event Details'),
        ('app/templates/client/commissions.html', 'Commission Tracking'),
        ('app/templates/customer/dashboard.html', 'Customer Dashboard'),
        ('app/templates/customer/browse_events.html', 'Browse Events'),
        ('app/templates/customer/event_detail.html', 'Event Details'),
        ('app/templates/customer/purchases.html', 'My Purchases'),
        ('app/templates/customer/review_event.html', 'Review Event'),
        ('app/templates/customer/my_reviews.html', 'My Reviews'),
    ]
    
    for template_path, page_title in template_files:
        if not Path(template_path).exists():
            content = base_template.replace('{{ page_title }}', page_title)
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Created {template_path}")
    
    print()
    
    # Summary
    print("=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python run.py")
    print("3. Open http://localhost:5000 in your browser")
    print("4. Register test accounts with different roles")
    print()
    print("For more details, see SETUP_GUIDE.md")
    print()

if __name__ == '__main__':
    try:
        setup_ticketzetu()
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        import traceback
        traceback.print_exc()
