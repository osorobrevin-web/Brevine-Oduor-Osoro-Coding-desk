#!/usr/bin/env python3
"""
Setup script for TICKETZETU Flask Application
Creates all necessary directories and files
"""
import os
import sys

base_path = r"c:\Users\User\Documents\Brevine Osoro Coding Desk.worktrees\agents-ticket-system-structure-admin-client"
os.chdir(base_path)

# Create directory structure
dirs = [
    "app",
    "app\\core",
    "app\\auth",
    "app\\admin",
    "app\\client",
    "app\\customer",
    "app\\templates",
    "app\\templates\\auth",
    "app\\templates\\admin",
    "app\\templates\\client",
    "app\\templates\\customer",
    "app\\templates\\components",
]

print("Creating directories...")
for d in dirs:
    os.makedirs(d, exist_ok=True)
    print(f"  ✓ {d}")

# Create __init__.py files for packages
print("\nCreating __init__.py files...")
init_locations = [
    "app\\__init__.py",
    "app\\core\\__init__.py",
    "app\\auth\\__init__.py",
    "app\\admin\\__init__.py",
    "app\\client\\__init__.py",
    "app\\customer\\__init__.py",
]

for init_file in init_locations:
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            module_name = os.path.dirname(init_file).split(os.sep)[-1]
            f.write(f"# {module_name} module\n")
        print(f"  ✓ {init_file}")

print("\n✅ Setup complete! All directories and __init__.py files created.")
print("\nNext step: Run 'pip install -r requirements.txt' to install dependencies")
print("Then: Run 'python run.py' to start the Flask application")
