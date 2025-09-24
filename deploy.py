#!/usr/bin/env python
"""
Deployment script for ERP Lite on PythonAnywhere
Run this script after uploading the project to PythonAnywhere
"""

import os
import sys
import subprocess

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("🚀 Starting ERP Lite deployment on PythonAnywhere...")

    # Get the current directory (should be the project root)
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Project directory: {project_dir}")

    # Install requirements
    print("\n📦 Installing requirements...")
    if not run_command("pip install -r requirements.txt"):
        print("❌ Failed to install requirements")
        return False

    # Run migrations
    print("\n🗄️ Running database migrations...")
    if not run_command("python manage.py migrate"):
        print("❌ Failed to run migrations")
        return False

    # Collect static files
    print("\n📄 Collecting static files...")
    if not run_command("python manage.py collectstatic --noinput"):
        print("❌ Failed to collect static files")
        return False

    # Create superuser (optional)
    print("\n👤 Creating superuser...")
    print("Note: You'll be prompted to create a superuser")
    try:
        subprocess.run("python manage.py createsuperuser", shell=True, cwd=project_dir)
    except:
        print("⚠️ Superuser creation skipped or failed")

    print("\n✅ Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Go to PythonAnywhere Web tab")
    print("2. Set up your web app with the correct paths")
    print("3. Configure environment variables:")
    print("   - DJANGO_SECRET_KEY: Generate a secure key")
    print("   - DJANGO_DEBUG: False")
    print("4. Reload your web app")
    print("\n🎉 Your ERP Lite should be live at erplite.pythonanywhere.com!")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)