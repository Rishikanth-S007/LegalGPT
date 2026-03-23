#!/usr/bin/env python3
"""
Test script to verify missing keyword fixes
"""
import sys
import os
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.services.law_predictor_service import predict_law

test_cases = [
    ("My boss slapped me in front of colleagues", "IPC 323-325 (Assault)", 1),
    ("My father-in-law physically abused my children", "DV Act + POCSO Act", 2),
    ("I lost money through a UPI fraud call", "IT Act 66C (Cybercrime)", 3),
    ("I am feeling sad today", "Out of Scope", 4),
    ("What is the capital of India", "Out of Scope", 5),
    ("Someone stole my gold chain", "IPC 378 (Theft) - Should still work", 6),
]

@pytest.mark.parametrize("query,expected_category,test_num", test_cases)
def test_query(query, expected_category, test_num):
    print(f"\n{'='*80}")
    print(f"TEST {test_num}: {query}")
    print(f"Expected: {expected_category}")
    print('='*80)
    result = predict_law(query)
    assert isinstance(result, dict), f"Unexpected result type: {type(result)}"

    applicable_law = result.get('structured_data', {}).get('applicable_law', result.get('applicable_law', 'N/A'))
    confidence = result.get('confidence', 0)
    legal_position = result.get('structured_data', {}).get('legal_position', result.get('legal_position', 'N/A'))

    print(f"[OK] Applicable Law: {applicable_law}")
    print(f"[OK] Confidence: {confidence:.2%}")
    print(f"[OK] Legal Position: {legal_position[:150]}...")

    assert 0.0 <= confidence <= 1.0, f"CONFIDENCE CHECK FAILED: {confidence} is outside [0, 1]"
    if "Out of Scope" not in expected_category:
        assert applicable_law != "Out of Scope", f"For input '{query}' got Out of Scope (should be {expected_category})"
    else:
        assert applicable_law == "Out of Scope", f"For input '{query}' should be Out of Scope, got {applicable_law}"
