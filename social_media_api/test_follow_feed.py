"""
Test script for Follow and Feed functionality
Run with: python test_follow_feed.py
Make sure the server is running: python manage.py runserver
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def register_user(username, email, password):
    """Register a user and return token"""
    url = f"{BASE_URL}/register/"
    data = {
        "username": username,
        "email": email,
        "password": password,
        "bio": f"I am {username}"
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return response.json().get('token'), response.json()['user']['id']
        else:
            # User might already exist, try login
            login_url = f"{BASE_URL}/login/"
            login_data = {"username": username, "password": password}
            response = requests.post(login_url, json=login_data)
            if response.status_code == 200:
                # Get user ID by fetching profile
                token = response.json().get('token')
                profile_url = f"{BASE_URL}/profile/"
                headers = {"Authorization": f"Token {token}"}
                profile_response = requests.get(profile_url, headers=headers)
                user_id = profile_response.json().get('id')
                return token, user_id
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def create_post(token, title, content):
    """Create a post and return post ID"""
    url = f"{BASE_URL}/posts/"
    headers = {"Authorization": f"Token {token}"}
    data = {
        "title": title,
        "content": content
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return response.json().get('id')
    except Exception as e:
        print(f"Error: {e}")
    return None

def test_follow_user(follower_token, user_to_follow_id):
    """Test following a user"""
    url = f"{BASE_URL}/follow/{user_to_follow_id}/"
    headers = {"Authorization": f"Token {follower_token}"}
    
    print(f"\n1. Testing Follow User {user_to_follow_id}...")
    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_unfollow_user(follower_token, user_to_unfollow_id):
    """Test unfollowing a user"""
    url = f"{BASE_URL}/unfollow/{user_to_unfollow_id}/"
    headers = {"Authorization": f"Token {follower_token}"}
    
    print(f"\n2. Testing Unfollow User {user_to_unfollow_id}...")
    try:
        response = requests.post(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_feed(token, expected_count=None):
    """Test retrieving the feed"""
    url = f"{BASE_URL}/feed/"
    headers = {"Authorization": f"Token {token}"}
    
    print(f"\n3. Testing Feed...")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Number of posts in feed: {len(data)}")
        
        if len(data) > 0:
            print(f"\nFirst post in feed:")
            print(f"  Title: {data[0].get('title')}")
            print(f"  Author: {data[0].get('author')}")
            print(f"  Created: {data[0].get('created_at')}")
        
        if expected_count is not None:
            if len(data) == expected_count:
                print(f"✓ Feed has expected {expected_count} posts")
            else:
                print(f"✗ Expected {expected_count} posts, got {len(data)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_feed_ordering(token):
    """Test that feed posts are ordered by creation date (most recent first)"""
    url = f"{BASE_URL}/feed/"
    headers = {"Authorization": f"Token {token}"}
    
    print(f"\n4. Testing Feed Ordering...")
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if len(data) >= 2:
            # Check if posts are in descending order by created_at
            dates = [post['created_at'] for post in data]
            is_ordered = all(dates[i] >= dates[i+1] for i in range(len(dates)-1))
            
            if is_ordered:
                print("✓ Feed posts are correctly ordered (most recent first)")
            else:
                print("✗ Feed posts are NOT correctly ordered")
            
            return is_ordered
        else:
            print("Not enough posts to test ordering")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_profile(token):
    """Test getting user profile with follower counts"""
    url = f"{BASE_URL}/profile/"
    headers = {"Authorization": f"Token {token}"}
    
    print(f"\n5. Testing Profile with Follow Counts...")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Username: {data.get('username')}")
        print(f"Followers: {data.get('followers_count')}")
        print(f"Following: {data.get('following_count')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("Follow and Feed Functionality Test Suite")
    print("=" * 70)
    print("\nMake sure the server is running: python manage.py runserver\n")
    
    # Create test users
    print("Setting up test users...")
    user1_token, user1_id = register_user("alice_follow", "alice@example.com", "testpass123")
    user2_token, user2_id = register_user("bob_follow", "bob@example.com", "testpass123")
    user3_token, user3_id = register_user("charlie_follow", "charlie@example.com", "testpass123")
    
    if not all([user1_token, user2_token, user3_token]):
        print("Failed to create test users. Exiting.")
        exit(1)
    
    print(f"✓ Created/Retrieved users:")
    print(f"  - Alice (ID: {user1_id})")
    print(f"  - Bob (ID: {user2_id})")
    print(f"  - Charlie (ID: {user3_id})")
    
    # Create posts for Bob and Charlie
    print("\nCreating test posts...")
    bob_post1 = create_post(user2_token, "Bob's First Post", "Hello from Bob!")
    bob_post2 = create_post(user2_token, "Bob's Second Post", "Another post by Bob")
    charlie_post = create_post(user3_token, "Charlie's Post", "Charlie here!")
    
    print(f"✓ Created posts")
    
    # Test 1: Alice's feed should be empty (not following anyone)
    print("\n" + "=" * 70)
    print("TEST SCENARIO 1: Empty Feed (not following anyone)")
    print("=" * 70)
    test_feed(user1_token, expected_count=0)
    
    # Test 2: Alice follows Bob
    print("\n" + "=" * 70)
    print("TEST SCENARIO 2: Follow User")
    print("=" * 70)
    test_follow_user(user1_token, user2_id)
    
    # Test 3: Alice's feed should show Bob's posts
    print("\n" + "=" * 70)
    print("TEST SCENARIO 3: Feed After Following")
    print("=" * 70)
    test_feed(user1_token, expected_count=2)
    
    # Test 4: Alice follows Charlie
    print("\n" + "=" * 70)
    print("TEST SCENARIO 4: Follow Another User")
    print("=" * 70)
    test_follow_user(user1_token, user3_id)
    
    # Test 5: Alice's feed should show posts from both Bob and Charlie
    print("\n" + "=" * 70)
    print("TEST SCENARIO 5: Feed with Multiple Followed Users")
    print("=" * 70)
    test_feed(user1_token, expected_count=3)
    test_feed_ordering(user1_token)
    
    # Test 6: Check Alice's profile
    print("\n" + "=" * 70)
    print("TEST SCENARIO 6: Profile with Follow Counts")
    print("=" * 70)
    test_profile(user1_token)
    
    # Test 7: Alice unfollows Bob
    print("\n" + "=" * 70)
    print("TEST SCENARIO 7: Unfollow User")
    print("=" * 70)
    test_unfollow_user(user1_token, user2_id)
    
    # Test 8: Alice's feed should only show Charlie's post
    print("\n" + "=" * 70)
    print("TEST SCENARIO 8: Feed After Unfollowing")
    print("=" * 70)
    test_feed(user1_token, expected_count=1)
    
    # Test 9: Try to follow yourself (should fail)
    print("\n" + "=" * 70)
    print("TEST SCENARIO 9: Cannot Follow Yourself")
    print("=" * 70)
    url = f"{BASE_URL}/follow/{user1_id}/"
    headers = {"Authorization": f"Token {user1_token}"}
    response = requests.post(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    if response.status_code == 400:
        print("✓ Correctly prevented self-follow")
    else:
        print("✗ Should have prevented self-follow")
    
    print("\n" + "=" * 70)
    print("All Tests Completed!")
    print("=" * 70)
    print("\nSummary:")
    print("- Follow/Unfollow functionality tested")
    print("- Feed generation and ordering verified")
    print("- Profile with follow counts checked")
    print("- Edge cases (self-follow) tested")
