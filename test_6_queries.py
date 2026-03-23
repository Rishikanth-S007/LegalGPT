#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script for 6 failing queries"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

# Test queries
test_queries = [
    {
        "query": "My husband beats me every night",
        "expected": ["DV Act", "498A", "Domestic"],
        "description": "TEST 1: Domestic Violence"
    },
    {
        "query": "A teacher sexually assaulted a 13 year old",
        "expected": ["POCSO", "376"],
        "description": "TEST 2: POCSO + Sexual Assault"
    },
    {
        "query": "Contractor took advance and disappeared",
        "expected": ["420", "406", "Fraud"],
        "description": "TEST 3: Fraud"
    },
    {
        "query": "My neighbor is encroaching on my land",
        "expected": ["Property"],
        "description": "TEST 4: Property Dispute"
    },
    {
        "query": "My phone stopped working after 2 days",
        "expected": ["Consumer", "CPA"],
        "description": "TEST 5: Consumer Issues"
    },
    {
        "query": "Someone tried to shoot me but I survived",
        "expected": ["307", "Attempt", "Murder"],
        "description": "TEST 6: Attempt to Murder"
    }
]

print("\n" + "="*80)
print("TESTING 6 FAILING QUERIES - KEYWORD FIX VERIFICATION")
print("="*80 + "\n")

passed = 0
failed = 0

for i, test in enumerate(test_queries, 1):
    print(f"{test['description']}")
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
        
        print(f"Result: {applicable_law}")
        print(f"Confidence: {confidence}")
        
        # Check if any expected keyword is in the result
        full_text = f"{applicable_law} {legal_position}".lower()
        found = []
        for keyword in test['expected']:
            if keyword.lower() in full_text:
                found.append(keyword)
        
        if found:
            print(f"[PASS] Found: {', '.join(found)}")
            passed += 1
        else:
            print(f"[FAIL] Expected one of: {', '.join(test['expected'])}")
            print(f"  Got: {applicable_law[:100]}")
            failed += 1
            
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        failed += 1
    
    print()

print("="*80)
print(f"RESULTS: {passed}/6 passed, {failed}/6 failed")
print("="*80 + "\n")
