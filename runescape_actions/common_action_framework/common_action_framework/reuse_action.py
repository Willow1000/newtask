def merge_dicts(d1, d2):
    """
    Recursively merge d2 into d1

    :param d1: The first dictionary (this will be modified if d2 is not None)
    :param d2: The second dictionary to merge into d1
    :return: The merged dictionary
    """
    for key, value in d2.items():
        if key in d1:
            if isinstance(d1[key], dict) and isinstance(value, dict):
                # If both d1[key] and d2[key] are dictionaries, merge them recursively
                d1[key] = merge_dicts(d1[key], value)
            else:
                # If d1[key] is not a dict or d2[key] is not a dict, replace d1[key] with d2[key]
                d1[key] = value
        else:
            # If the key is not in d1, just add it
            d1[key] = value
    return d1

def update_step(step, step_update=None):
    if step_update is not None:
        merge_dicts(step, step_update)

def update_action(action_ordered_steps, updates) -> list[dict]:
    """
    Update multiple steps in the action's ordered steps based on a list of updates
    each element in the updates list is also a step dictionary, identified by the "id" key, everything in this step will 
     override or be merged into the original step with the same id in the action_ordered_steps list

    :param action_ordered_steps: The list of steps from the action we want to update
    :param updates: A list of dictionaries, each one being an update for a specific step, identified by the "id"
    :return: Updated action ordered steps
    """
    for update in updates:
        step_id = update.get("id")

        # Find the step with the specified step_id
        step = next((s for s in action_ordered_steps if s["id"] == step_id), None)
        if step:
            # Update the step using the provided parameters
            update_step(step, update)
        else:
            print(f"Step with id '{step_id}' not found in the provided action steps.")

    return action_ordered_steps

