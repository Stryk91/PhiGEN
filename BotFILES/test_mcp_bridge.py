#!/usr/bin/env python3
"""
Test script for MCP Bridge
Validates all endpoints and functionality
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8765"

def test_health():
    """Test health endpoint"""
    print("\n1. Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {data.get('status')}")
            print(f"   ✓ Service: {data.get('service')}")
            return True
        else:
            print(f"   ✗ Failed with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ✗ Connection failed - is the bridge running?")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_list_tools():
    """Test list tools endpoint"""
    print("\n2. Testing List Tools...")
    try:
        response = requests.get(f"{BASE_URL}/mcp/tools", timeout=5)
        if response.status_code == 200:
            data = response.json()
            tools = data.get('tools', [])
            print(f"   ✓ Found {len(tools)} tools:")
            for tool in tools:
                print(f"      - {tool['name']}: {tool['description']}")
            return True
        else:
            print(f"   ✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_status():
    """Test status endpoint"""
    print("\n3. Testing Status Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/mcp/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Status: {data.get('status')}")
            print(f"   ✓ Queue Size: {data.get('queue_size')}")
            print(f"   ✓ Feed Entries: {data.get('feed_entries')}")
            print(f"   ✓ BotFiles Dir: {data.get('botfiles_dir')}")
            return True
        else:
            print(f"   ✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_send_message():
    """Test sending a message"""
    print("\n4. Testing Send Message...")
    try:
        payload = {
            "tool": "discord_send_message",
            "parameters": {
                "message": f"Test message from MCP at {datetime.now().strftime('%H:%M:%S')}"
            }
        }
        response = requests.post(
            f"{BASE_URL}/mcp/execute",
            json=payload,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success: {data.get('success')}")
            print(f"   ✓ Result: {data.get('result')}")
            return True
        else:
            print(f"   ✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_check_jc():
    """Test checking JC status"""
    print("\n5. Testing Check JC Status...")
    try:
        payload = {
            "tool": "discord_check_jc_status",
            "parameters": {}
        }
        response = requests.post(
            f"{BASE_URL}/mcp/execute",
            json=payload,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success: {data.get('success')}")
            result = data.get('result', {})
            if 'error' in result:
                print(f"   ! No JC activity: {result.get('error')}")
            else:
                print(f"   ✓ JC Agent: {result.get('agent')}")
                print(f"   ✓ Action: {result.get('action')}")
            return True
        else:
            print(f"   ✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_read_feed():
    """Test reading agent feed"""
    print("\n6. Testing Read Feed...")
    try:
        payload = {
            "tool": "discord_read_feed",
            "parameters": {
                "limit": 3
            }
        }
        response = requests.post(
            f"{BASE_URL}/mcp/execute",
            json=payload,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success: {data.get('success')}")
            result = data.get('result', [])
            if isinstance(result, list):
                print(f"   ✓ Retrieved {len(result)} entries")
                for entry in result:
                    agent = entry.get('agent', 'unknown')
                    action = entry.get('action', 'unknown')
                    print(f"      - [{agent}] {action}")
            return True
        else:
            print(f"   ✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_list_botfiles():
    """Test listing BotFILES"""
    print("\n7. Testing List BotFiles...")
    try:
        payload = {
            "tool": "discord_list_botfiles",
            "parameters": {}
        }
        response = requests.post(
            f"{BASE_URL}/mcp/execute",
            json=payload,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Success: {data.get('success')}")
            result = data.get('result', [])
            print(f"   ✓ Found {len(result)} items:")
            for item in result[:5]:
                name = item.get('name')
                item_type = item.get('type')
                size = item.get('size')
                if size:
                    print(f"      - {name} ({item_type}, {size} bytes)")
                else:
                    print(f"      - {name} ({item_type})")
            return True
        else:
            print(f"   ✗ Failed with status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("MCP Bridge Test Suite")
    print("=" * 60)

    tests = [
        test_health,
        test_list_tools,
        test_status,
        test_send_message,
        test_check_jc,
        test_read_feed,
        test_list_botfiles
    ]

    results = []
    for test in tests:
        results.append(test())
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("Test Results")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
    else:
        print(f"✗ {total - passed} test(s) failed")

    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
