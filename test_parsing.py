#!/usr/bin/env python3
"""Test script for carryover parsing functionality."""

from vyakarana.models import SutraCarryover, CarryoverType

# Test anuvritti parsing
print("Testing anuvritti parsing:")
anuvritti_text = "वृद्धिः$11001##गुणः$11002"
anuvritti = SutraCarryover.from_string(anuvritti_text, CarryoverType.ANUVRITTI)
print(f"Combined text: {anuvritti.combined_text}")
print(f"Type: {anuvritti.carryover_type}")
print(f"References count: {len(anuvritti.references)}")
for i, ref in enumerate(anuvritti.references):
    print(f'  Reference {i+1}: "{ref.text_portion}" -> {ref.reference_string}')

print()

# Test adhikara parsing
print("Testing adhikara parsing:")
adhikara_text = "आकडारात् एका संज्ञा$1$4$1"
adhikara = SutraCarryover.from_string(adhikara_text, CarryoverType.ADHIKARA)
print(f"Combined text: {adhikara.combined_text}")
print(f"Type: {adhikara.carryover_type}")
print(f"References count: {len(adhikara.references)}")
for i, ref in enumerate(adhikara.references):
    print(f'  Reference {i+1}: "{ref.text_portion}" -> {ref.reference_string}')
