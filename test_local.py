#!/usr/bin/env python3
"""
Local test script to verify deployment package works
Run: python3 test_local.py
"""

import os
import json

def test_data_loading():
    """Test that data file can be found and loaded"""
    print("Testing data loading...")

    # Simulate webhook_server.py path resolution
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data', 'hafh_stories.json')

    print(f"  Looking for: {data_path}")

    if not os.path.exists(data_path):
        print(f"  ❌ FAILED: File not found")
        return False

    print(f"  ✅ File exists")

    # Load and verify
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"  ❌ FAILED: Expected list, got {type(data)}")
        return False

    print(f"  ✅ Loaded {len(data)} properties")

    if len(data) != 10230:
        print(f"  ⚠️  WARNING: Expected 10,230 properties, got {len(data)}")

    # Verify structure of first property
    if data:
        prop = data[0]
        required_fields = ['name', 'prefecture', 'country']
        missing = [f for f in required_fields if f not in prop]
        if missing:
            print(f"  ❌ FAILED: Missing fields: {missing}")
            return False
        print(f"  ✅ Data structure valid")

    return True

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")

    required_files = [
        'webhook_server.py',
        'requirements.txt',
        'render.yaml',
        'README.md',
        'data/hafh_stories.json'
    ]

    for filepath in required_files:
        exists = os.path.exists(filepath)
        status = "✅" if exists else "❌"
        print(f"  {status} {filepath}")
        if not exists:
            return False

    return True

def test_requirements():
    """Test that requirements.txt has necessary packages"""
    print("\nTesting requirements.txt...")

    with open('requirements.txt', 'r') as f:
        content = f.read()

    required_packages = ['flask', 'flask-cors', 'gunicorn']

    for package in required_packages:
        if package in content.lower():
            print(f"  ✅ {package}")
        else:
            print(f"  ❌ Missing: {package}")
            return False

    return True

def main():
    print("="*60)
    print("KABUK Webhook Server - Deployment Package Test")
    print("="*60)

    tests = [
        ("File Structure", test_file_structure),
        ("Requirements", test_requirements),
        ("Data Loading", test_data_loading)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results.append((name, False))

    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)

    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("✅ All tests passed! Ready to deploy.")
        print("\nNext steps:")
        print("1. Push to GitHub: git init && git add . && git commit -m 'Initial'")
        print("2. Deploy on Render: https://dashboard.render.com/")
        print("3. Update ElevenLabs webhook URL")
        return 0
    else:
        print("❌ Some tests failed. Fix issues before deploying.")
        return 1

if __name__ == '__main__':
    exit(main())
