#!/usr/bin/env python3
"""Test script for real sutra data parsing."""

from vyakarana import read_sutras

collection = read_sutras("sutraani/data.txt")

print("Testing with real sutra data:")
print("=" * 40)

# Test a complex anuvritti example
for sutra in collection:
    if sutra.has_anuvritti and len(sutra.anuvritti.references) > 2:
        print(f"Sutra: {sutra.reference}")
        print(f"Original anuvritti text: {sutra.anuvritti.combined_text}")
        print(f"Parsed references: {len(sutra.anuvritti.references)}")
        for i, ref in enumerate(sutra.anuvritti.references):
            print(f'  {i+1}. "{ref.text_portion}" from {ref.reference_string}')
        break

print()

# Test a complex adhikara example
for sutra in collection:
    if sutra.has_adhikara and len(sutra.adhikara.references) > 1:
        print(f"Sutra: {sutra.reference}")
        print(f"Original adhikara text: {sutra.adhikara.combined_text}")
        print(f"Parsed references: {len(sutra.adhikara.references)}")
        for i, ref in enumerate(sutra.adhikara.references):
            print(f'  {i+1}. "{ref.text_portion}" from {ref.reference_string}')
        break

print()

# Show some statistics
total_anuvritti = sum(1 for s in collection if s.has_anuvritti)
total_adhikara = sum(1 for s in collection if s.has_adhikara)
total_anuvritti_refs = sum(
    len(s.anuvritti.references) for s in collection if s.has_anuvritti
)
total_adhikara_refs = sum(
    len(s.adhikara.references) for s in collection if s.has_adhikara
)

print("Parsing Statistics:")
print(f"Total sutras with anuvritti: {total_anuvritti}")
print(f"Total sutras with adhikara: {total_adhikara}")
print(f"Total anuvritti references parsed: {total_anuvritti_refs}")
print(f"Total adhikara references parsed: {total_adhikara_refs}")
