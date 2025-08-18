#!/usr/bin/env python3
"""
Setup script for Side Wind Django project
"""

import os
import sys
import subprocess
import secrets

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def create_env_file():
    """Create .env file with default settings"""
    env_content = f"""# Django Settings
SECRET_KEY={secrets.token_urlsafe(50)}
DEBUG=True

# Database (for production, use PostgreSQL)
DATABASE_URL=sqlite:///db.sqlite3

# Stripe Settings (get these from your Stripe dashboard)
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Email Settings (for production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 Settings (for production file storage)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with default settings")

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists('sidewind_env'):
        print("✅ Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    result = run_command('python -m venv sidewind_env')
    if result is not None:
        print("✅ Virtual environment created")
        return True
    else:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("Installing dependencies...")
    
    # Determine the correct pip command
    if os.name == 'nt':  # Windows
        pip_cmd = 'sidewind_env\\Scripts\\pip'
    else:  # Unix/Linux/macOS
        pip_cmd = 'sidewind_env/bin/pip'
    
    result = run_command(f'{pip_cmd} install -r requirements.txt')
    if result is not None:
        print("✅ Dependencies installed")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False

def run_migrations():
    """Run Django migrations"""
    print("Running migrations...")
    
    # Determine the correct python command
    if os.name == 'nt':  # Windows
        python_cmd = 'sidewind_env\\Scripts\\python'
    else:  # Unix/Linux/macOS
        python_cmd = 'sidewind_env/bin/python'
    
    result = run_command(f'{python_cmd} manage.py makemigrations')
    if result is not None:
        print("✅ Created migrations")
    
    result = run_command(f'{python_cmd} manage.py migrate')
    if result is not None:
        print("✅ Applied migrations")
        return True
    else:
        print("❌ Failed to run migrations")
        return False

def create_superuser():
    """Create a superuser account"""
    print("\n" + "="*50)
    print("SUPERUSER CREATION")
    print("="*50)
    print("You can create a superuser account now or later using:")
    print("python manage.py createsuperuser")
    print("="*50)

def main():
    """Main setup function"""
    print("🚀 Setting up Side Wind Django project...")
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Run migrations
    if not run_migrations():
        sys.exit(1)
    
    # Create superuser
    create_superuser()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate the virtual environment:")
    if os.name == 'nt':  # Windows
        print("   sidewind_env\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print("   source sidewind_env/bin/activate")
    print("2. Update the .env file with your actual settings")
    print("3. Create a superuser: python manage.py createsuperuser")
    print("4. Run the development server: python manage.py runserver")
    print("5. Visit http://127.0.0.1:8000/ to see your website")
    print("\nFor deployment instructions, see README.md")

if __name__ == '__main__':
    main()
