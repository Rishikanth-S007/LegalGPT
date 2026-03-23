#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify LegalGPT fixes
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

# Test queries for all 3 issues
test_queries = [
    {
        "query": "Contractor took money and ran",
        "expected_contains": ["IPC", "420", "406", "Fraud"],
        "description": "ISSUE 1: Fraud - contractor took money"
    },
    {
        "query": "Hit pedestrian with my car",
        "expected_contains": ["Motor Vehicle", "184"],
        "description": "ISSUE 2: Motor Vehicles - hit pedestrian"
    },
    {
        "query": "Insurance rejected my claim",
        "expected_contains": ["Consumer Protection Act 2019", "Section 2(11)", "edaakhil"],
        "expected_NOT": "analyzing applicable laws",
        "description": "ISSUE 3: Consumer - full CPA 2019 details"
    },
    {
        "query": "My laptop was stolen from my bag",
        "expected_contains": ["IPC", "378"],
        "description": "Previously working: Theft"
    },
    {
        "query": "Someone hacked my bank account",
        "expected_contains": ["IT Act", "Cyber"],
        "description": "Previously working: Cybercrime"
    },
    {
        "query": "Gun found in house",
        "expected_contains": ["Arms Act"],
        "description": "Previously working: Arms Act"
    },
    {
        "query": "Teacher scolded me",
        "expected_law": "Out of Scope",
        "description": "Previously working: Out of Scope"
    }
]

print("\n" + "="*80)
print("TESTING LEGALGPT FIXES FOR 3 ISSUES")
print("="*80 + "\n")

passed = 0
failed = 0

for i, test in enumerate(test_queries, 1):
    print(f"\nTest {i}: {test['description']}")
    print(f"Query: '{test['query']}'")
    print("-" * 80)
    
    try:
        response = requests.post(
            "http://localhost:8000/api/predict",
            json={"query": test['query']},
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"[FAIL] HTTP Error: {response.status_code}")
            failed += 1
            continue
            
        data = response.json()
        result = data.get('response', {})
        
        applicable_law = result.get('applicable_law', 'N/A')
        legal_position = result.get('legal_position', '')
        confidence = result.get('confidence', 0)
        
        print(f"Applicable Law: {applicable_law}")
        print(f"Confidence: {confidence}")
        
        # Check expected law
        if 'expected_law' in test:
            if applicable_law == test['expected_law']:
                print(f"✓ PASS - Correctly identified as {test['expected_law']}")
                passed += 1
            else:
                print(f"✗ FAIL - Expected {test['expected_law']}, got {applicable_law}")
                failed += 1
        
        # Check expected contains
        elif 'expected_contains' in test:
            full_text = f"{applicable_law} {legal_position}".lower()
            missing = []
            for keyword in test['expected_contains']:
                if keyword.lower() not in full_text:
                    missing.append(keyword)
            
            if not missing:
                print(f"✓ PASS - All keywords found: {', '.join(test['expected_contains'])}")
                passed += 1
            else:
                print(f"✗ FAIL - Missing keywords: {', '.join(missing)}")
                failed += 1
        
        # Check expected NOT (for consumer placeholder check)
        if 'expected_NOT' in test:
            if test['expected_NOT'].lower() in legal_position.lower():
                print(f"✗ FAIL - Found unwanted text: '{test['expected_NOT']}'")
                print(f"    Legal Position: {legal_position[:100]}...")
                # Don't increment failed twice
            else:
                print(f"✓ Generic placeholder NOT present")
                
    except Exception as e:
        print(f"✗ FAIL - Error: {e}")
        failed += 1

print("\n" + "="*80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_queries)} tests")
print("="*80 + "\n")
