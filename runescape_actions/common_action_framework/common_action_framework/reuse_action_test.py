# Import functions from reuse_action.py
from reuse_action import merge_dicts, update_step, update_action
import copy

if __name__ == "__main__":
        # Test merge_dicts function with various data types

    D1 = {
        'camp1': {
            'camp2': 'abc',
            'camp3': 'cbd',
            'camp4': {
                'camp5': 'def'
            }
        },
        'camp10': [1, 2, 3],  # List example
        'camp11': 42,          # Integer example
        'camp12': 'string1'    # String example
    }

    D2 = {
        'camp1': {
            'camp9': 'dawdw',
            'camp2': 'ddddd',
            'camp4': {
                'camp5': 'defed',
                'camp6': 'dedaw'
            }
        },
        'camp10': [4, 5, 6],   # List example to be replaced
        'camp11': 100,         # Integer example to be replaced
        'camp12': 'string2',   # String example to be replaced
        'camp13': 'new_key'    # New key to be added
    }

    # Merge D2 into D1
    merge_result = merge_dicts(D1, D2)

    # Print the merged dictionary
    print("Merged Dictionary:")
    print(merge_result)

    # Test update_action function

    action_steps = [
        {"id": 1, "check": "check1", "verify": "verify1", "check_args": {"arg1": 1}},
        {"id": 2, "check": "check2", "verify": "verify2", "check_args": {"arg2": 2}},
    ]

    updates = [
        {"id": 1, "check": "new_check1", "verify": "new_verify1", "check_args": {"arg1": 10}},
        {"id": 2, "check": "new_check2", "verify": "new_verify2", "check_args": {"arg2": 20}, "verify_args": {"arg3": 30}},
        {"id": 3, "check": "new_check3"}  # This step_id does not exist
    ]

    updated_steps = update_action(action_steps, updates)

    print("\nUpdated Action Steps:")
    print(updated_steps)
