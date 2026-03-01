"""
Verification script to check if all requirements are met
"""
import os
import re

def check_file_contains(filepath, patterns, description):
    """Check if file contains all specified patterns"""
    print(f"\n{'='*70}")
    print(f"Checking: {description}")
    print(f"File: {filepath}")
    print(f"{'='*70}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_found = True
    for pattern in patterns:
        if isinstance(pattern, str):
            if pattern in content:
                print(f"✅ Found: {pattern}")
            else:
                print(f"❌ Missing: {pattern}")
                all_found = False
        else:  # regex pattern
            if re.search(pattern, content):
                print(f"✅ Found pattern: {pattern.pattern}")
            else:
                print(f"❌ Missing pattern: {pattern.pattern}")
                all_found = False
    
    return all_found

def main():
    print("\n" + "="*70)
    print("SOCIAL MEDIA API - REQUIREMENTS VERIFICATION")
    print("="*70)
    
    results = []
    
    # Check 1: accounts/views.py contains required patterns
    results.app