import os
import sys
import json
import argparse
from typing import Dict, List, Tuple

# -------------------------------
# Import comparison tool at module level
# -------------------------------
project_path = os.environ.get("path_containing_LocallyAvailableTooling")
if not project_path:
    raise EnvironmentError("path_containing_LocallyAvailableTooling not set.")

tooling_path = os.path.join(project_path, "LocallyAvailableActionTooling")
sys.path.append(tooling_path)

try:
    from compare_specific_image_list_to_other_base_image import compare_icon_to_image_list, MatchingAlgorithm
except ImportError as e:
    raise ImportError(f"Failed to import comparison tool: {e}")

# -------------------------------
# Core Functions
# -------------------------------
def resolve_path(image_path: str, section: str) -> str:
    """Resolve image path based on section type."""
    if not image_path.startswith("all/"):
        return image_path

    rest = image_path.split("all/", 1)[1]
    
    if rest.startswith("0common_photos"):
        return os.path.join("commons", rest)

    first_folder = rest.split("/", 1)[0]
    image_name = rest.split("/")[-1]
    folder_type = "action" if section == "icons" else "test"

    return os.path.join(
        "commons", first_folder, "all_action_files", "screenshots", 
        folder_type, image_name
    )


def evaluate_comparison(icon_path: str, test_path: str) -> Tuple[bool, float]:
    """Compare icon against test image and return result."""
    try:
        _, result = compare_icon_to_image_list(
            icon_image=icon_path,
            background_images_to_find_icon_in=[test_path],
            algorithm=MatchingAlgorithm.TEMPLATE_MATCH,
            precision=0.8
        )
        
        if result and len(result) >= 3:
            match_x, _, precision_value = result
            return match_x >= 0, round(float(precision_value), 2)
        return False, 0.0
    except Exception:
        return False, 0.0


def run_comparisons(action_name: str) -> Dict[str, List[Dict]]:
    """Run comparisons for an action and return grouped results."""
    action_name = action_name.lower()

    # Locate mapping file
    if action_name.startswith("all/"):
        mapping_file = os.path.join("commons", action_name.split("all/", 1)[1], "mapping.json")
    else:
        mapping_file = os.path.join(action_name, "mapping.json")

    if not os.path.exists(mapping_file):
        raise FileNotFoundError(f"Mapping file not found: {mapping_file}")

    with open(mapping_file) as f:
        mapping = json.load(f)

    comparisons = mapping.get("comparisons", {})
    icons = mapping.get("icons", {})
    tests = mapping.get("tests", {})

    if not comparisons:
        raise ValueError("No comparisons defined in mapping.json")

    # Collect results
    grouped_results = {}
    for icon_label, test_ids in comparisons.items():
        if isinstance(test_ids, str):
            test_ids = [test_ids]
            
        if icon_label not in icons:
            continue

        icon_path = resolve_path(icons[icon_label], "icons")
        icon_name = os.path.basename(icon_path)

        for test_id in test_ids:
            if test_id not in tests:
                continue

            test_path = resolve_path(tests[test_id], "tests")
            test_name = os.path.basename(test_path)
            passed, precision = evaluate_comparison(icon_path, test_path)

            if icon_label not in grouped_results:
                grouped_results[icon_label] = []

            grouped_results[icon_label].append({
                "icon_name": icon_name,
                "test_id": test_id,
                "test_name": test_name,
                "passed": passed,
                "precision": precision
            })

    return grouped_results


def format_results(grouped_results: Dict[str, List[Dict]]) -> str:
    """Format results in the required 3-line format per icon."""
    if not grouped_results:
        return "No results to display."
    
    output = []
    for icon_label, results in grouped_results.items():
        if not results:
            continue
            
        icon_name = results[0]["icon_name"]
        passed_tests = [f'"{r["test_id"]}"' for r in results if r["passed"]]
        failed_tests = [f'{r["test_name"]} {r["precision"]:.2f}' for r in results if not r["passed"]]
        
        output.append(f'"{icon_name}":')
        output.append(f'PASS: {", ".join(passed_tests)}' if passed_tests else "PASS:")
        output.append(f'FAILED: {", ".join(failed_tests)}' if failed_tests else "FAILED:")
        output.append("")  # Blank line between icons
    
    return "\n".join(output)


# -------------------------------
# Main execution
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run comparisons from mapping")
    parser.add_argument("action", help="Action name (e.g., superheat or all/superheat)")
    args = parser.parse_args()

    try:
        results = run_comparisons(args.action)
        print(format_results(results))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)