"""
Test MongoDB Integration
Verifies all services are connected to MongoDB and working correctly
"""

import asyncio
import httpx
from datetime import datetime

# Service URLs
SERVICES = {
    "auth": "http://localhost:8001",
    "text": "http://localhost:8002",
    "voice": "http://localhost:8003",
    "face": "http://localhost:8004",
    "fusion": "http://localhost:8005",
}

async def test_service_health(name, url):
    """Test if a service is healthy"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name.upper():15} - Status: {data.get('status', 'unknown')}, DB: {data.get('database', 'unknown')}")
                return True
            else:
                print(f"❌ {name.upper():15} - HTTP {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ {name.upper():15} - Error: {str(e)[:50]}")
        return False

async def test_mongodb_connection():
    """Test MongoDB connection directly"""
    try:
        from backend.shared.mongodb import check_connection
        result = await check_connection()
        if result:
            print("✅ MongoDB Direct Connection - OK")
        else:
            print("❌ MongoDB Direct Connection - Failed")
        return result
    except Exception as e:
        print(f"❌ MongoDB Direct Connection - Error: {str(e)}")
        return False

async def test_text_analysis():
    """Test text analysis with MongoDB"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{SERVICES['text']}/v1/analyze/text",
                json={
                    "user_id": "test_user_123",
                    "text": "I feel anxious and worried about the future"
                }
            )
            if response.status_code == 200:
                data = response.json()
                result = data.get("result", {})
                print(f"✅ Text Analysis      - Emotion: {result.get('emotion_label')}, Score: {result.get('emotion_score')}")
                return True
            else:
                print(f"❌ Text Analysis      - HTTP {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Text Analysis      - Error: {str(e)[:50]}")
        return False

async def test_emotion_history():
    """Test emotion history retrieval"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{SERVICES['text']}/v1/analyze/emotion/history",
                params={"user_id": "test_user_123", "days": 7}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Emotion History    - Found {data.get('count', 0)} records")
                return True
            else:
                print(f"❌ Emotion History    - HTTP {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Emotion History    - Error: {str(e)[:50]}")
        return False

async def main():
    """Run all tests"""
    print("=" * 70)
    print("MongoDB Integration Test Suite")
    print("=" * 70)
    print()
    
    print("📊 Testing Service Health Endpoints...")
    print("-" * 70)
    health_results = []
    for name, url in SERVICES.items():
        result = await test_service_health(name, url)
        health_results.append(result)
        await asyncio.sleep(0.2)
    
    print()
    print("📊 Testing MongoDB Direct Connection...")
    print("-" * 70)
    mongo_result = await test_mongodb_connection()
    
    print()
    print("📊 Testing Functional Endpoints...")
    print("-" * 70)
    text_result = await test_text_analysis()
    await asyncio.sleep(0.5)
    history_result = await test_emotion_history()
    
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    total_tests = len(health_results) + 3  # health + mongo + text + history
    passed_tests = sum(health_results) + sum([mongo_result, text_result, history_result])
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print("=" * 70)
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! MongoDB integration is working correctly.")
    elif passed_tests >= total_tests * 0.7:
        print("⚠️  Most tests passed. Check failed services above.")
    else:
        print("❌ Many tests failed. Please check service logs and MongoDB connection.")

if __name__ == "__main__":
    asyncio.run(main())
