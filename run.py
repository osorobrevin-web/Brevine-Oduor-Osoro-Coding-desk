"""
TICKETZETU Flask Application
Main entry point
"""
import os
import sys

print("Setting up application structure...")

# Create app directory structure
base_path = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(base_path, 'app')

os.makedirs(os.path.join(app_path, 'core'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'auth'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'admin'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'client'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'customer'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'templates', 'auth'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'templates', 'admin'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'templates', 'client'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'templates', 'customer'), exist_ok=True)
os.makedirs(os.path.join(app_path, 'templates', 'components'), exist_ok=True)

print("✓ Directory structure created")

# Now create __init__.py files
init_files = [
    os.path.join(app_path, '__init__.py'),
    os.path.join(app_path, 'core', '__init__.py'),
    os.path.join(app_path, 'auth', '__init__.py'),
    os.path.join(app_path, 'admin', '__init__.py'),
    os.path.join(app_path, 'client', '__init__.py'),
    os.path.join(app_path, 'customer', '__init__.py'),
]

for init_file in init_files:
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write(f"# {os.path.basename(os.path.dirname(init_file))} module\n")

print("✓ __init__.py files created")

from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    print("\n🚀 Starting TICKETZETU Flask Application...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
