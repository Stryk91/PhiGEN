"""
Test Multi-Model System
Verify Mistral, Granite, and Claude routing works correctly
"""

import os
import sys
from model_router import ModelRouter


def test_router_initialization():
    """Test router initializes correctly"""
    print("1. Testing Router Initialization...")
    try:
        router = ModelRouter()
        print("   ✅ Router initialized")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_model_status():
    """Test model availability"""
    print("\n2. Checking Model Status...")
    router = ModelRouter()
    status = router.get_status()

    results = []
    for name, info in status.items():
        available = "✅" if info['available'] else "❌"
        cost = "FREE" if info['cost_per_1m'] == 0 else f"${info['cost_per_1m']}/1M"
        print(f"   {available} {info['name']}: {cost} ({info['provider']})")
        results.append(info['available'])

    return any(results)  # At least one model should be available


def test_mistral():
    """Test Mistral generation"""
    print("\n3. Testing Mistral...")
    router = ModelRouter()

    if not router._is_available(router.MODELS['mistral']):
        print("   ⚠️  Mistral not available (pull with: ollama pull mistral:7b-instruct-q4_K_M)")
        return False

    try:
        response, model = router.route("Say 'Mistral works!' in one sentence", model="mistral")
        print(f"   Response: {response[:100]}")
        print("   ✅ Mistral working")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_granite():
    """Test Granite generation"""
    print("\n4. Testing Granite...")
    router = ModelRouter()

    if not router._is_available(router.MODELS['granite']):
        print("   ⚠️  Granite not available (pull with: ollama pull granite-code:3b)")
        return False

    try:
        response, model = router.route("Say 'Granite works!' in one sentence", model="granite")
        print(f"   Response: {response[:100]}")
        print("   ✅ Granite working")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_claude():
    """Test Claude API"""
    print("\n5. Testing Claude API...")
    router = ModelRouter()

    if not router.anthropic_api_key:
        print("   ⚠️  Claude not configured (set ANTHROPIC_API_KEY in .env)")
        return False

    try:
        response, model = router.route("Say 'Claude works!' in one sentence", model="claude")
        print(f"   Response: {response[:100]}")
        print("   ✅ Claude working")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_smart_routing():
    """Test automatic model selection"""
    print("\n6. Testing Smart Routing...")
    router = ModelRouter()

    test_cases = [
        ("How do I fix this Python error?", "code"),
        ("Tell me a joke", "chat"),
        ("Analyze this algorithm's complexity", "analysis")
    ]

    results = []
    for prompt, expected_type in test_cases:
        try:
            response, model = router.route(prompt, task_type=expected_type)
            print(f"   {expected_type}: routed to {model.name} ✅")
            results.append(True)
        except Exception as e:
            print(f"   {expected_type}: failed - {e} ❌")
            results.append(False)

    return all(results)


def test_comparison():
    """Test model comparison"""
    print("\n7. Testing Model Comparison...")
    router = ModelRouter()

    try:
        results = router.compare_models("Say your name in one word", models=["mistral", "granite"])

        for model_name, response in results.items():
            status = "✅" if not response.startswith("❌") else "⚠️"
            print(f"   {status} {model_name}: {response[:50]}")

        print("   ✅ Comparison working")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_usage_tracking():
    """Test usage statistics"""
    print("\n8. Testing Usage Tracking...")
    router = ModelRouter()

    try:
        stats = router.get_stats()
        print(f"   Total requests: {stats['total_requests']}")
        print(f"   Estimated savings: ${stats['estimated_savings']}")
        print("   ✅ Usage tracking working")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Multi-Model System Test Suite")
    print("=" * 60)

    tests = [
        ("Router Initialization", test_router_initialization),
        ("Model Status", test_model_status),
        ("Mistral Generation", test_mistral),
        ("Granite Generation", test_granite),
        ("Claude API", test_claude),
        ("Smart Routing", test_smart_routing),
        ("Model Comparison", test_comparison),
        ("Usage Tracking", test_usage_tracking)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ Test crashed: {e}")
            results.append((name, False))

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<40} {status}")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    print(f"\nPassed: {passed_count}/{total_count}")

    if passed_count >= 6:
        print("\n🎉 Multi-model system is working!")
        print("\nNext steps:")
        print("  1. Pull missing models if needed")
        print("  2. Start Discord bot: docker-compose --profile ai up -d")
        print("  3. Test in Discord: !help_ai")
    else:
        print("\n⚠️  Some tests failed. Check:")
        print("  - Ollama is running: docker-compose ps | grep ollama")
        print("  - Models are pulled: docker exec phigen-ollama ollama list")
        print("  - ANTHROPIC_API_KEY is set in .env")

    return passed_count >= 6


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
