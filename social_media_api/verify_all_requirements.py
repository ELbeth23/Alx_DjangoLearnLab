"""
Comprehensive verification script for ALL requirements
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

print("="*70)
print("COMPREHENSIVE REQUIREMENTS VERIFICATION")
print("="*70)
print()

all_results = []

# TASK 0: User Authentication
print("TASK 0: User Authentication")
print("="*70)
all_results.append(check_pattern(
    'accounts/serializers.py',
    'get_user_model().objects.create_user',
    'Serializer uses get_user_model().objects.create_user'
))
all_results.append(check_pattern(
    'accounts/urls.py',
    "path('register/'",
    'Registration URL exists'
))
all_results.append(check_pattern(
    'accounts/urls.py',
    "path('login/'",
    'Login URL exists'
))
all_results.append(check_pattern(
    'accounts/urls.py',
    "path('profile/'",
    'Profile URL exists'
))

# TASK 1: Posts and Comments
print("\nTASK 1: Posts and Comments")
print("="*70)
all_results.append(check_pattern(
    'social_media_api/urls.py',
    "path('api/'",
    'Main URLs use api/ prefix'
))
all_results.append(check_pattern(
    'posts/views.py',
    'class PostViewSet(viewsets.ModelViewSet)',
    'PostViewSet uses ModelViewSet'
))
all_results.append(check_pattern(
    'posts/views.py',
    'class CommentViewSet(viewsets.ModelViewSet)',
    'CommentViewSet uses ModelViewSet'
))
all_results.append(check_pattern(
    'posts/views.py',
    'IsOwnerOrReadOnly',
    'Uses IsOwnerOrReadOnly permission'
))

# TASK 2: Follow and Feed
print("\nTASK 2: Follow and Feed")
print("="*70)
all_results.append(check_pattern(
    'accounts/views.py',
    'permissions.IsAuthenticated',
    'Follow views use permissions.IsAuthenticated'
))
all_results.append(check_pattern(
    'accounts/views.py',
    'CustomUser.objects.all()',
    'Follow views use CustomUser.objects.all()'
))
all_results.append(check_pattern(
    'accounts/views.py',
    'def follow_user',
    'follow_user function exists'
))
all_results.append(check_pattern(
    'accounts/views.py',
    'def unfollow_user',
    'unfollow_user function exists'
))
all_results.append(check_pattern(
    'accounts/urls.py',
    "path('follow/<int:user_id>/'",
    'Follow URL pattern exists'
))
all_results.append(check_pattern(
    'accounts/urls.py',
    "path('unfollow/<int:user_id>/'",
    'Unfollow URL pattern exists'
))
all_results.append(check_pattern(
    'posts/views.py',
    'def feed',
    'Feed function exists'
))
all_results.append(check_pattern(
    'posts/views.py',
    'Post.objects.filter(author__in=following_users).order_by',
    'Feed uses following_users with order_by'
))
all_results.append(check_pattern(
    'posts/urls.py',
    "path('feed/'",
    'Feed URL pattern exists'
))

# TASK 3: Likes and Notifications
print("\nTASK 3: Likes and Notifications")
print("="*70)
all_results.append(check_pattern(
    'posts/views.py',
    'generics.get_object_or_404(Post, pk=pk)',
    'Like views use generics.get_object_or_404'
))
all_results.append(check_pattern(
    'posts/views.py',
    'Like.objects.get_or_create(user=request.user, post=post)',
    'Like view uses get_or_create with correct params'
))
all_results.append(check_pattern(
    'posts/urls.py',
    "path('posts/<int:pk>/like/'",
    'Like URL pattern exists'
))
all_results.append(check_pattern(
    'posts/urls.py',
    "path('posts/<int:pk>/unlike/'",
    'Unlike URL pattern exists'
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
    print("\n🎉 ALL REQUIREMENTS MET! 🎉")
    print("\nYour Social Media API is fully implemented!")
else:
    print(f"\n⚠️  {total - passed} requirement(s) still need attention")

print("\n" + "="*70)
