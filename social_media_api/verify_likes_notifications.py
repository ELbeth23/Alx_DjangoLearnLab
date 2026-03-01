"""
Verification script for Likes and Notifications requirements
"""
import os

def check_pattern(filepath, pattern, description):
    """Check if file contains pattern"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    found = pattern in content
    status = "✅" if found else "❌"
    print(f"{status} {description}")
    if not found:
        print(f"   Missing pattern: {pattern}")
    print()
    return found

print("="*70)
print("LIKES AND NOTIFICATIONS - REQUIREMENTS VERIFICATION")
print("="*70)
print()

results = []

# Requirement 1: Like/Unlike views with specific patterns
print("Requirement 1: Like/Unlike views in posts app")
print("-"*70)
results.append(check_pattern(
    'posts/views.py',
    'permissions.IsAuthenticated',
    'Uses permissions.IsAuthenticated'
))
results.append(check_pattern(
    'posts/views.py',
    'generics.get_object_or_404(Post, pk=pk)',
    'Uses generics.get_object_or_404(Post, pk=pk)'
))
results.append(check_pattern(
    'posts/views.py',
    'Like.objects.get_or_create(user=request.user, post=post)',
    'Uses Like.objects.get_or_create(user=request.user, post=post)'
))

# Requirement 2: URL patterns for like/unlike
print("Requirement 2: Like/Unlike URL patterns in posts")
print("-"*70)
results.append(check_pattern(
    'posts/urls.py',
    "path('posts/<int:pk>/like/'",
    'Like URL pattern exists'
))
results.append(check_pattern(
    'posts/urls.py',
    "path('posts/<int:pk>/unlike/'",
    'Unlike URL pattern exists'
))

# Summary
print("="*70)
print("SUMMARY")
print("="*70)
passed = sum(results)
total = len(results)
print(f"\nPassed: {passed}/{total} checks")

if passed == total:
    print("\n✅ ALL LIKES/NOTIFICATIONS REQUIREMENTS MET!")
else:
    print(f"\n❌ {total - passed} requirement(s) still not met")

print()
