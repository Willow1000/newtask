import os
import json
import string
from itertools import product
import argparse
from typing import Dict, List, Optional
from collections import Counter

def generate_mapping(base_action_folder: str) -> Dict:
    """
    Generate mapping for a given action folder with precise pairing logic.
    Returns the mapping dictionary.
    """
    base_action_folder = base_action_folder.lower()

    # Resolve base folder
    if base_action_folder.startswith("all/"):
        base_action_folder_name = os.path.join("commons", base_action_folder.split("all/", 1)[1])
    else:
        base_action_folder_name = base_action_folder

    action_dir = os.path.join(base_action_folder_name, "all_action_files/screenshots/action")
    test_dir = os.path.join(base_action_folder_name, "all_action_files/screenshots/test")

    mapping = {"icons": {}, "tests": {}, "comparisons": {}}

    # Label generator (A-Z, AA-ZZ...)
    def generate_labels(n: int) -> List[str]:
        letters = string.ascii_uppercase
        result = []
        # Single letters
        for l in letters:
            result.append(l)
            if len(result) >= n:
                return result
        # Double letters
        for pair in product(letters, repeat=2):
            result.append("".join(pair))
            if len(result) >= n:
                return result
        return result

    # Load and map images
    action_images = sorted([f for f in os.listdir(action_dir) if f.endswith(".png")])
    test_images = sorted([f for f in os.listdir(test_dir) if f.endswith(".png")])

    labels = generate_labels(len(action_images))
    for label, img in zip(labels, action_images):
        mapping["icons"][label] = os.path.join(action_dir, img)

    for i, img in enumerate(test_images, 1):
        mapping["tests"][str(i)] = os.path.join(test_dir, img)

    # Normalize names for comparison
    def normalize(filename: str) -> str:
        return os.path.splitext(filename)[0].lower()

    normalized_actions = {label: normalize(img) for label, img in zip(labels, action_images)}
    normalized_tests = {str(i): normalize(img) for i, img in enumerate(test_images, 1)}

    # Refined Category Extraction Logic:
    # A suffix is only a category if it appears at least twice in the current action folder.
    suffixes = []
    for a_name in normalized_actions.values():
        parts = a_name.split('_')
        if len(parts) > 1:
            suffixes.append(parts[-1])
    
    suffix_counts = Counter(suffixes)
    valid_categories = {s for s, count in suffix_counts.items() if count >= 2}

    def extract_category(full_name: str) -> tuple:
        parts = full_name.split('_')
        if len(parts) > 1:
            suffix = parts[-1]
            if suffix in valid_categories:
                return suffix, '_'.join(parts[:-1])  # category, base_name
            else:
                return None, '_'.join(parts[:-1]) # No category, but still has a base_name
        return None, full_name

    # Process actions
    action_categories = {}
    for label, a_name in normalized_actions.items():
        category, base_name = extract_category(a_name)
        action_categories[label] = {
            "base_name": base_name, "category": category, "full_name": a_name
        }

    # Identify global tests (only test_items and test_withdraw_items)
    global_test_ids = [
        t_id for t_id, t_name in normalized_tests.items()
        if t_name in ["test_items", "test_withdraw_items"]
    ]

    # Build comparisons
    for label, info in action_categories.items():
        matched_tests = set(global_test_ids)  # Start with global tests

        for t_id, t_name in normalized_tests.items():
            if t_id in matched_tests:
                continue

            # Category matches (only if category is valid/recurring)
            if info["category"] and t_name in [f"test_{info['category']}"]:
                matched_tests.add(t_id)
                continue

            # Full name matches
            if t_name in [f"test_{info['full_name']}"]:
                matched_tests.add(t_id)
                continue

            # Base name matches
            if t_name in [f"test_{info['base_name']}"]:
                matched_tests.add(t_id)
                continue

        mapping["comparisons"][label] = sorted(matched_tests)  # Sort for consistency

    return mapping


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate mapping for an action folder")
    parser.add_argument("action", help="Action name (example: superheat or all/superheat)")
    args = parser.parse_args()

    mapping = generate_mapping(args.action)

    # Save mapping JSON
    if args.action.startswith("all/"):
        save_folder = os.path.join("commons", args.action.split("all/", 1)[1])
    else:
        save_folder = args.action

    os.makedirs(save_folder, exist_ok=True)
    mapping_file_path = os.path.join(save_folder, "mapping.json")

    with open(mapping_file_path, "w") as f:
        json.dump(mapping, f, indent=4)

    # Summary output
    print(f"\nMapping generated: {mapping_file_path}")
    print(f"Icons: {len(mapping['icons'])}")
    print(f"Tests: {len(mapping['tests'])}")
    print(f"Comparisons: {len(mapping['comparisons'])}")

    # Quick verification of categories
    icon_names = [os.path.basename(p) for p in mapping['icons'].values()]
    suffixes = [n.replace('.png', '').split('_')[-1] for n in icon_names if '_' in n]
    suffix_counts = Counter(suffixes)
    valid_categories = sorted([s for s, count in suffix_counts.items() if count >= 2])

    if valid_categories:
        print(f"\nDetected recurring categories (count >= 2): {valid_categories}")
    else:
        print("\nNo recurring categories detected.")

    # Sample mappings
    print("\nSample mappings (first 3):")
    for label, test_ids in list(mapping['comparisons'].items())[:3]:
        icon_name = os.path.basename(mapping['icons'][label])
        test_names = [os.path.basename(mapping['tests'][tid]) for tid in test_ids[:2]]
        if len(test_ids) > 2:
            test_names.append("...")
        print(f"  {label} ({icon_name}) -> {test_names}")

    # Global tests
    global_tests = [
        os.path.basename(mapping['tests'][tid])
        for tid in mapping['tests']
        if os.path.basename(mapping['tests'][tid]) in ["test_items.png", "test_withdraw_items.png"]
    ]
    if global_tests:
        print(f"\nGlobal tests: {global_tests}")
