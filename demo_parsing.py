#!/usr/bin/env python3
"""
Comprehensive demonstration of the Sanskrit sutra parsing functionality.

This script showcases the complete parsing implementation for anuvritti and adhikara
carryover references, demonstrating how complex Sanskrit grammatical references
are parsed into structured data.
"""

from vyakarana import read_sutras


def main():
    """Main function to run the parsing demonstration."""

    print("🔬 Sanskrit Sutra Carryover Parsing Demo")
    print("=" * 50)

    # Load the sutra collection
    collection = read_sutras("sutraani/data.txt")

    # Demo 1: Anuvritti parsing
    print("\n📜 ANUVRITTI PARSING EXAMPLE")
    print("-" * 30)

    # Find a sutra with complex anuvritti
    for sutra in collection:
        if sutra.has_anuvritti and len(sutra.anuvritti.references) >= 3:
            print(f"Sutra: {sutra.reference} - {sutra.sanskrit}")
            print(f"Raw anuvritti text: {sutra.anuvritti.combined_text}")
            print(f"Parsed into {len(sutra.anuvritti.references)} references:")

            for i, ref in enumerate(sutra.anuvritti.references, 1):
                print(
                    f"  {i}. Text: '{ref.text_portion}' from sutra {ref.reference_string}"
                )
            break

    # Demo 2: Adhikara parsing
    print("\n📋 ADHIKARA PARSING EXAMPLE")
    print("-" * 30)

    # Find a sutra with complex adhikara
    for sutra in collection:
        if sutra.has_adhikara and len(sutra.adhikara.references) >= 2:
            print(f"Sutra: {sutra.reference} - {sutra.sanskrit}")
            print(f"Raw adhikara text: {sutra.adhikara.combined_text}")
            print(f"Parsed into {len(sutra.adhikara.references)} references:")

            for i, ref in enumerate(sutra.adhikara.references, 1):
                print(
                    f"  {i}. Text: '{ref.text_portion}' from sutra {ref.reference_string}"
                )
            break

    # Demo 3: Statistics
    print("\n📊 PARSING STATISTICS")
    print("-" * 30)

    # Calculate comprehensive statistics
    total_sutras = len(collection)
    anuvritti_sutras = sum(1 for s in collection if s.has_anuvritti)
    adhikara_sutras = sum(1 for s in collection if s.has_adhikara)
    both_carryover = sum(1 for s in collection if s.has_anuvritti and s.has_adhikara)

    total_anuvritti_refs = sum(len(s.anuvritti.references) for s in collection)
    total_adhikara_refs = sum(len(s.adhikara.references) for s in collection)

    # Distribution of reference counts
    anuvritti_counts = {}
    adhikara_counts = {}

    for sutra in collection:
        an_count = len(sutra.anuvritti.references)
        ad_count = len(sutra.adhikara.references)

        anuvritti_counts[an_count] = anuvritti_counts.get(an_count, 0) + 1
        adhikara_counts[ad_count] = adhikara_counts.get(ad_count, 0) + 1

    print(f"Total sutras: {total_sutras}")
    print(
        f"Sutras with anuvritti: {anuvritti_sutras} ({anuvritti_sutras/total_sutras*100:.1f}%)"
    )
    print(
        f"Sutras with adhikara: {adhikara_sutras} ({adhikara_sutras/total_sutras*100:.1f}%)"
    )
    print(
        f"Sutras with both: {both_carryover} ({both_carryover/total_sutras*100:.1f}%)"
    )
    print()
    print(f"Total anuvritti references parsed: {total_anuvritti_refs}")
    print(f"Total adhikara references parsed: {total_adhikara_refs}")
    print(
        f"Average anuvritti refs per sutra: {total_anuvritti_refs/anuvritti_sutras:.2f}"
    )
    print(f"Average adhikara refs per sutra: {total_adhikara_refs/adhikara_sutras:.2f}")

    # Demo 4: Format examples
    print("\n🔍 PARSING FORMAT PATTERNS")
    print("-" * 30)

    print("Anuvritti format: text$adhyaya+pada+number##text$adhyaya+pada+number##...")
    print("Example: 'वृद्धिः$11001##गुणः$11002' → 2 references")
    print("  - 'वृद्धिः' from sutra 1.1.1")
    print("  - 'गुणः' from sutra 1.1.2")
    print()
    print("Adhikara format: text$adhyaya$pada$number##text$adhyaya$pada$number##...")
    print("Example: 'आकडारात् एका संज्ञा$1$4$1##कारके$1$4$23' → 2 references")
    print("  - 'आकडारात् एका संज्ञा' from sutra 1.4.1")
    print("  - 'कारके' from sutra 1.4.23")

    print(
        "\n✅ Parsing complete! The Sanskrit carryover references are now fully structured."
    )
    print(
        "🎯 Achievement: 'The biggie' - complete anuvritti and adhikara parsing implemented!"
    )


if __name__ == "__main__":
    main()
