"""
Quick Setup Helper
Run this script to set up the job scraper system quickly
"""

import os
import sys
from pathlib import Path

def setup_config():
    """Interactive setup for configuration"""
    print("\n📋 Job Scraper Setup\n")
    print("="*60)
    
    # Email setup
    print("\n📧 Email Configuration (Optional for alerts)")
    email = input("Enter Gmail address (press Enter to skip): ").strip()
    
    if email:
        print("\n⚠️  Use Gmail App Password, NOT your regular password!")
        print("See README.md for instructions to generate App Password")
        app_password = input("Enter 16-character App Password: ").strip()
        
        config_updates = {
            'EMAIL': f'"{email}"',
            'PASSWORD': f'"{app_password}"',
            'RECIPIENT_EMAIL': f'"{email}"',
            'SEND_EMAIL_ALERTS': 'True'
        }
    else:
        config_updates = {
            'SEND_EMAIL_ALERTS': 'False'
        }
    
    # Location setup
    location = input("\nTarget location for jobs (default 'India'): ").strip() or "India"
    config_updates['LOCATION'] = f'"{location}"'
    
    # Scheduler setup
    schedule_enabled = input("\nEnable daily scheduler? (y/n, default n): ").strip().lower() == 'y'
    config_updates['ENABLE_SCHEDULER'] = str(schedule_enabled)
    
    if schedule_enabled:
        schedule_time = input("Daily run time (HH:MM, default 09:00): ").strip() or "09:00"
        config_updates['SCHEDULE_TIME'] = f'"{schedule_time}"'
    
    return config_updates

def update_config_file(updates):
    """Update config.py with user inputs"""
    config_path = Path("utils/config.py")
    
    if not config_path.exists():
        print("❌ utils/config.py not found!")
        return False
    
    try:
        content = config_path.read_text()
        
        for key, value in updates.items():
            # Simple replacement
            pattern = f'{key} = '
            if pattern in content:
                # Find the line and replace it
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if pattern in line:
                        # Get indentation
                        indent = len(line) - len(line.lstrip())
                        lines[i] = ' ' * indent + f'{key} = {value}'
                        break
                content = '\n'.join(lines)
        
        config_path.write_text(content)
        print("✅ Config updated successfully!")
        return True
    
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'requests',
        'bs4',
        'pandas',
        'openpyxl',
        'lxml',
        'schedule'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages with:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def main():
    """Main setup flow"""
    print("\n🚀 Welcome to Job Scraper System Setup!\n")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)
    
    # Interactive config setup
    updates = setup_config()
    
    # Update config file
    print("\n💾 Saving configuration...")
    if update_config_file(updates):
        print("\n"+("="*60))
        print("✅ Setup Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Review utils/config.py to customize skills")
        print("2. Run: python main.py")
        print("3. Check output/ folder for results")
        print("\nFor detailed instructions, see README.md")
    else:
        print("\n❌ Setup failed. Please check config.py manually")
        sys.exit(1)

if __name__ == "__main__":
    main()
