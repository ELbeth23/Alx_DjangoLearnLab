"""
Verification script for Deployment requirements
"""
import os

def check_pattern(filepath, pattern, description):
    """Check if file contains pattern"""
    if not os.path.exists(filepath):
        print(f"❌ {description}")
        print(f"   File not found: {filepath}")
        print()
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    found = pattern in content
    status = "✅" if found else "❌"
    print(f"{status} {description}")
    if not found:
        print(f"   Missing: {pattern}")
    print()
    return found

def check_file_exists(filepath, description):
    """Check if file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    if not exists:
        print(f"   File not found: {filepath}")
    print()
    return exists

print("="*70)
print("DEPLOYMENT REQUIREMENTS VERIFICATION")
print("="*70)
print()

all_results = []

# Task 4: Deployment Configuration
print("TASK 4: Deployment Configuration")
print("="*70)

# Requirement 1: Production settings
print("\n1. Production Settings")
print("-"*70)
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'DEBUG = False',
    'DEBUG set to False'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'ALLOWED_HOSTS',
    'ALLOWED_HOSTS configured'
))

# Requirement 2: Security settings
print("\n2. Security Settings")
print("-"*70)
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'SECURE_BROWSER_XSS_FILTER',
    'SECURE_BROWSER_XSS_FILTER configured'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'X_FRAME_OPTIONS',
    'X_FRAME_OPTIONS configured'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'SECURE_CONTENT_TYPE_NOSNIFF',
    'SECURE_CONTENT_TYPE_NOSNIFF configured'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'SECURE_SSL_REDIRECT',
    'SECURE_SSL_REDIRECT configured'
))

# Requirement 3: Database credentials
print("\n3. Database Configuration")
print("-"*70)
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'DB_USER',
    'DB_USER environment variable support'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'DB_PASSWORD',
    'DB_PASSWORD environment variable support'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'DB_HOST',
    'DB_HOST environment variable support'
))

# Requirement 4: Static files and S3
print("\n4. Static Files and AWS S3 Configuration")
print("-"*70)
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'STATIC_ROOT',
    'STATIC_ROOT configured for collectstatic'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'USE_S3',
    'AWS S3 configuration available'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'AWS_STORAGE_BUCKET_NAME',
    'AWS S3 bucket configuration'
))
all_results.append(check_pattern(
    'social_media_api/settings.py',
    'collectstatic',
    'collectstatic mentioned in comments/docs'
))

# Deployment files
print("\n5. Deployment Files")
print("-"*70)
all_results.append(check_file_exists(
    'requirements.txt',
    'requirements.txt exists'
))
all_results.append(check_file_exists(
    '.env.example',
    '.env.example exists'
))
all_results.append(check_file_exists(
    'Procfile',
    'Procfile exists (Heroku)'
))
all_results.append(check_file_exists(
    'runtime.txt',
    'runtime.txt exists'
))
all_results.append(check_file_exists(
    '.gitignore',
    '.gitignore exists'
))
all_results.append(check_file_exists(
    'DEPLOYMENT.md',
    'DEPLOYMENT.md documentation exists'
))

# Summary
print("\n" + "="*70)
print("FINAL SUMMARY")
print("="*70)

passed = sum(all_results)
total = len(all_results)

print(f"\nTotal Checks: {total}")
print(f"Passed: {passed}")
print(f"Failed: {total - passed}")
print(f"Success Rate: {(passed/total)*100:.1f}%")

if passed == total:
    print("\n🎉 ALL DEPLOYMENT REQUIREMENTS MET! 🎉")
    print("\nYour Social Media API is ready for production deployment!")
else:
    print(f"\n⚠️  {total - passed} requirement(s) still need attention")

print("\n" + "="*70)
print("\nNext Steps:")
print("1. Review DEPLOYMENT.md for detailed deployment instructions")
print("2. Set up environment variables (.env file)")
print("3. Choose a hosting platform (Heroku, AWS, DigitalOcean, etc.)")
print("4. Run: python manage.py collectstatic")
print("5. Deploy your application")
print("="*70)
