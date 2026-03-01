"""
Test script for Posts and Comments API endpoints
Run with: python test_posts_comments.py
Make sure the server is running: python manage.py runserver
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def register_test_user():
    """Register a test user and return token"""
    url = f"{BASE_URL}/register/"
    data = {
        "username": "testuser_posts",
        "email": "testposts@example.com",
        "password": "testpass123",
        "bio": "Testing posts and comments"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('token')
        else:
            # User might already exist, try login
            login_url = f"{BASE_URL}/login/"
            login_data = {"username": "testuser_posts", "password": "testpass123"}
            response = requests.post(login_url, json=login_data)
            return response.json().get('token')
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_create_post(token):
    """Test creating a post"""
    url = f"{BASE_URL}/posts/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": "Test Post",
        "content": "This is a test post content"
    }
    
    print("\n1. Testing Create Post...")
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json().get('id')
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_list_posts():
    """Test listing all posts"""
    url = f"{BASE_URL}/posts/"
    
    print("\n2. Testing List Posts...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            print(f"Total Posts: {data.get('count')}")
            print(f"Posts on this page: {len(data.get('results', []))}")
        else:
            print(f"Posts: {len(data)}")
    except Exception as e:
        print(f"Error: {e}")

def test_get_post(post_id):
    """Test retrieving a single post"""
    url = f"{BASE_URL}/posts/{post_id}/"
    
    print(f"\n3. Testing Get Post {post_id}...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_update_post(post_id, token):
    """Test updating a post"""
    url = f"{BASE_URL}/posts/{post_id}/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": "Updated Test Post",
        "content": "This content has been updated"
    }
    
    print(f"\n4. Testing Update Post {post_id}...")
    try:
        response = requests.patch(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_search_posts():
    """Test searching posts"""
    url = f"{BASE_URL}/posts/?search=test"
    
    print("\n5. Testing Search Posts...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            print(f"Found {len(data.get('results', []))} posts matching 'test'")
        else:
            print(f"Found {len(data)} posts")
    except Exception as e:
        print(f"Error: {e}")

def test_create_comment(post_id, token):
    """Test creating a comment"""
    url = f"{BASE_URL}/comments/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "post": post_id,
        "content": "This is a test comment"
    }
    
    print(f"\n6. Testing Create Comment on Post {post_id}...")
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.json().get('id')
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_list_comments():
    """Test listing all comments"""
    url = f"{BASE_URL}/comments/"
    
    print("\n7. Testing List Comments...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            print(f"Total Comments: {data.get('count')}")
        else:
            print(f"Comments: {len(data)}")
    except Exception as e:
        print(f"Error: {e}")

def test_update_comment(comment_id, token):
    """Test updating a comment"""
    url = f"{BASE_URL}/comments/{comment_id}/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "content": "This comment has been updated"
    }
    
    print(f"\n8. Testing Update Comment {comment_id}...")
    try:
        response = requests.patch(url, json=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_delete_comment(comment_id, token):
    """Test deleting a comment"""
    url = f"{BASE_URL}/comments/{comment_id}/"
    headers = {"Authorization": f"Token {token}"}
    
    print(f"\n9. Testing Delete Comment {comment_id}...")
    try:
        response = requests.delete(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 204:
            print("Comment deleted successfully")
    except Exception as e:
        print(f"Error: {e}")

def test_permissions(post_id):
    """Test that unauthenticated users cannot edit posts"""
    url = f"{BASE_URL}/posts/{post_id}/"
    data = {"title": "Trying to hack"}
    
    print(f"\n10. Testing Permissions (should fail)...")
    try:
        response = requests.patch(url, json=data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 401 or response.status_code == 403:
            print("✓ Permissions working correctly - unauthorized access denied")
        else:
            print("✗ Warning: Unauthorized access was allowed!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Posts and Comments API Test Suite")
    print("=" * 60)
    print("\nMake sure the server is running: python manage.py runserver\n")
    
    # Register/login user
    token = register_test_user()
    if not token:
        print("Failed to get authentication token. Exiting.")
        exit(1)
    
    print(f"\n✓ Authentication successful. Token: {token[:20]}...")
    
    # Test Posts
    post_id = test_create_post(token)
    test_list_posts()
    
    if post_id:
        test_get_post(post_id)
        test_update_post(post_id, token)
        test_search_posts()
        
        # Test Comments
        comment_id = test_create_comment(post_id, token)
        test_list_comments()
        
        if comment_id:
            test_update_comment(comment_id, token)
            test_delete_comment(comment_id, token)
        
        # Test Permissions
        test_permissions(post_id)
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)
    print("\nNote: The test post was not deleted. You can delete it manually")
    print(f"or via: DELETE /api/posts/{post_id}/ with your token")
