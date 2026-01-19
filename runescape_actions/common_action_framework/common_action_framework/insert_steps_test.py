from insert_steps import step_inserter


if __name__ == "__main__":
    # Example step to insert
    step_to_insert = [
        {
            "id": "new_step",
        }
    ]
    step_0 = {
        "id": "check_app_state_in_game_lobby",
    }

    # Step 1: Click the banker
    step_1 = {
        "id": "click_banker",
    }

    # Step 2: Click the "continue" option
    step_2 = {
        "id": "click_continue",
    }

    # Step 3: Click the "access my bank account option
    step_3 = {
        "id": "access_bank_account",
    }

    # Initial action ordered steps
    action_ordered_steps = [
        step_0,
        step_1,
        step_2,
        step_3,
    ]

    # Call step_inserter to insert the new step after "click_banker"
    new_action_ordered_steps = step_inserter(action_ordered_steps, "click_banker", step_to_insert)

    # Print the global namespace (to see dynamically created step_0, step_1, etc.)
    print(globals())

    # Print the result after insertion
    for step in new_action_ordered_steps:
        print(step["id"])