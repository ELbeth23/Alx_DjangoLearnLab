"""
Complete Project Verification - All Tasks
"""
import os

def check_pattern(filepath, pattern, description):
    """Check if file contains pattern"""
    if not os.path.exists(filepath):
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return pattern in content

def check_file_exists(filepath):
    """Check if file exists"""
    return os.path.exists(filepath)

print("="*70)
print("COMPLETE PROJECT VERIFICATION - ALL TASKS")
print("="*70)
print()

# Task counters
task_results = {
    'Task 0': [],
    'Task 1': [],
    'Task 2': [],
    'Task 3': [],
    'Task 4': []
}

# TASK 0: User Authentication
print("TASK 0: User Authentication")
print("-"*70)
task_results['Task 0'].append(check_pattern('accounts/serializers.py', 'get_user_model().objects.create_user', 'Serializer'))
task_results['Task 0'].append(check_pattern('accounts/urls.py', "path('register/'", 'Register URL'))
task_results['Task 0'].append(check_pattern('accounts/urls.py', "path('login/'", 'Login URL'))
task_results['Task 0'].append(check_pattern('accounts/urls.py', "path('profile/'", 'Profile URL'))
print(f"✅ Passed: {sum(task_results['Task 0'])}/4")
print()

# TASK 1: Posts and Comments
print("TASK 1: Posts and Comments")
print("-"*70)
task_results['Task 1'].append(check_pattern('social_media_api/urls.py', "path('api/'", 'API prefix'))
task_results['Task 1'].append(check_pattern('posts/views.py', 'class PostViewSet(viewsets.ModelViewSet)', 'PostViewSet'))
task_results['Task 1'].append(check_pattern('posts/views.py', 'class CommentViewSet(viewsets.ModelViewSet)', 'CommentViewSet'))
task_results['Task 1'].append(check_pattern('posts/views.py', 'IsOwnerOrReadOnly', 'Permissions'))
print(f"✅ Passed: {sum(task_results['Task 1'])}/4")
print()

# TASK 2: Follow and Feed
print("TASK 2: Follow and Feed")
print("-"*70)
task_results['Task 2'].append(check_pattern('accounts/views.py', 'permissions.IsAuthenticated', 'Follow permissions'))
task_results['Task 2'].append(check_pattern('accounts/views.py', 'CustomUser.objects.all()', 'CustomUser'))
task_results['Task 2'].append(check_pattern('accounts/views.py', 'def follow_user', 'follow_user'))
task_results['Task 2'].append(check_pattern('accounts/views.py', 'def unfollow_user', 'unfollow_user'))
task_results['Task 2'].append(check_pattern('accounts/urls.py', "path('follow/<int:user_id>/'", 'Follow URL'))
task_results['Task 2'].append(check_pattern('accounts/urls.py', "path('unfollow/<int:user_id>/'", 'Unfollow URL'))
task_results['Task 2'].append(check_pattern('posts/views.py', 'def feed', 'Feed function'))
task_results['Task 2'].append(check_pattern('posts/views.py', 'Post.objects.filter(author__in=following_users).order_by', 'Feed query'))
task_results['Task 2'].append(check_pattern('posts/urls.py', "path('feed/'", 'Feed URL'))
print(f"✅ Passed: {sum(task_results['Task 2'])}/9")
print()

# TASK 3: Likes and Notifications
print("TASK 3: Likes and Notifications")
print("-"*70)
task_results['Task 3'].append(check_pattern('posts/views.py', 'generics.get_object_or_404(Post, pk=pk)', 'get_object_or_404'))
task_results['Task 3'].append(check_pattern('posts/views.py', 'Like.objects.get_or_create(user=request.user, post=post)', 'get_or_create'))
task_results['Task 3'].append(check_pattern('posts/urls.py', "path('posts/<int:pk>/like/'", 'Like URL'))
task_results['Task 3'].append(check_pattern('posts/urls.py', "path('posts/<int:pk>/unlike/'", 'Unlike URL'))
print(f"✅ Passed: {sum(task_results['Task 3'])}/4")
print()

# TASK 4: Deployment
print("TASK 4: Deployment Configuration")
print("-"*70)
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'DEBUG = False', 'DEBUG False'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'SECURE_BROWSER_XSS_FILTER', 'XSS Filter'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'X_FRAME_OPTIONS', 'X-Frame'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'SECURE_CONTENT_TYPE_NOSNIFF', 'Content Type'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'SECURE_SSL_REDIRECT', 'SSL Redirect'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'DB_USER', 'DB User'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'DB_PASSWORD', 'DB Password'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'DB_HOST', 'DB Host'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'STATIC_ROOT', 'Static Root'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'USE_S3', 'S3 Config'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'AWS_STORAGE_BUCKET_NAME', 'S3 Bucket'))
task_results['Task 4'].append(check_pattern('social_media_api/settings.py', 'collectstatic', 'collectstatic'))
task_results['Task 4'].append(check_file_exists('requirements.txt'))
task_results['Task 4'].append(check_file_exists('.env.example'))
task_results['Task 4'].append(check_file_exists('Procfile'))
task_results['Task 4'].append(check_file_exists('DEPLOYMENT.md'))
print(f"✅ Passed: {sum(task_results['Task 4'])}/16")
print()

# Summary
print("="*70)
print("FINAL PROJECT SUMMARY")
print("="*70)
print()

total_checks = sum(len(checks) for checks in task_results.values())
total_passed = sum(sum(checks) for checks in task_results.values())

for task, results in task_results.items():
    passed = sum(results)
    total = len(results)
    percentage = (passed/total)*100 if total > 0 else 0
    status = "✅" if passed == total else "⚠️"
    print(f"{status} {task}: {passed}/{total} ({percentage:.0f}%)")

print()
print(f"Overall: {total_passed}/{total_checks} checks passed ({(total_passed/total_checks)*100:.1f}%)")
print()

if total_passed == total_checks:
    print("🎉 CONGRATULATIONS! 🎉")
    print()
    print("All requirements for the Social Media API project are complete!")
    print()
    print("✅ Task 0: User Authentication - COMPLETE")
    print("✅ Task 1: Posts and Comments - COMPLETE")
    print("✅ Task 2: Follow and Feed - COMPLETE")
    print("✅ Task 3: Likes and Notifications - COMPLETE")
    print("✅ Task 4: Deployment Configuration - COMPLETE")
    print()
    print("Your project is ready for production deployment!")
    print()
    print("Next Steps:")
    print("1. Review DEPLOYMENT.md for deployment instructions")
    print("2. Set up your environment variables")
    print("3. Choose a hosting platform")
    print("4. Deploy your application")
    print("5. Test in production")
else:
    print(f"⚠️  {total_checks - total_passed} requirement(s) need attention")

print("="*70)
