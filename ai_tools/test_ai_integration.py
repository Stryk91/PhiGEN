"""
Test script for AI integration
Run this to verify everything is working
"""

import sys
import time
from ollama_client import OllamaClient


def test_ollama_connection():
    """Test basic Ollama connection"""
    print("1. Testing Ollama connection...")
    client = OllamaClient()

    if client.is_available():
        print("   ✅ Ollama is running")
        return True
    else:
        print(f"   ❌ Ollama not available at {client.host}")
        return False


def test_model_availability():
    """Test if Granite model is available"""
    print("\n2. Checking models...")
    client = OllamaClient()

    try:
        models = client.list_models()
        print(f"   Available models: {models}")

        if "granite-4.0-h-micro:latest" in models:
            print("   ✅ Granite model found")
            return True
        else:
            print("   ⚠️  Granite model not found. Pull it with:")
            print("      docker exec phigen-ollama ollama pull granite-4.0-h-micro:latest")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_generation():
    """Test text generation"""
    print("\n3. Testing text generation...")
    client = OllamaClient()

    try:
        response = client.generate("Say 'AI is working!' in one sentence", max_tokens=50)
        print(f"   Response: {response[:100]}")
        print("   ✅ Generation working")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_api():
    """Test REST API"""
    print("\n4. Testing REST API...")
    import requests

    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ API is responding")
            print(f"   {response.json()}")
            return True
        else:
            print(f"   ❌ API returned {response.status_code}")
            return False
    except Exception as e:
        print(f"   ⚠️  API not accessible (may not be running): {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("PhiGEN AI Integration Test")
    print("=" * 60)

    results = []
    results.append(("Ollama Connection", test_ollama_connection()))
    time.sleep(1)
    results.append(("Model Availability", test_model_availability()))
    time.sleep(1)
    results.append(("Text Generation", test_generation()))
    time.sleep(1)
    results.append(("REST API", test_api()))

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<40} {status}")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    print(f"\nPassed: {passed_count}/{total_count}")

    if passed_count == total_count:
        print("\n🎉 All tests passed! AI integration is working.")
    elif passed_count >= 2:
        print("\n⚠️  Some tests failed. Check the output above.")
    else:
        print("\n❌ Multiple failures. Make sure services are running:")
        print("   docker-compose --profile ai up -d")

    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
