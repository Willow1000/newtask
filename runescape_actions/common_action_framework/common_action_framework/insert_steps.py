def step_inserter(action_ordered_steps, step_id, ordered_steps_to_insert):
    # Identify the index of the step where we want to insert the new steps
    if isinstance(step_id, int):
        # If step_id is an integer, we use it directly as the position
        insert_index = step_id
    else:
        # If step_id is a string, we find the index of the step with the matching "id"
        insert_index = next((i for i, step in enumerate(action_ordered_steps) if step["id"] == step_id), None)
        if insert_index is None:
            raise ValueError(f"Step with id '{step_id}' not found.")

    # Insert the ordered_steps_to_insert after the identified step
    insert_index += 1  # To insert after the step, we increment the index by 1

    # Shift the subsequent steps forward and insert the new steps
    new_steps = action_ordered_steps[:insert_index] + ordered_steps_to_insert + action_ordered_steps[insert_index:]

    return new_steps