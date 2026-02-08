import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "use_spell"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


# Step 1: Select Spellbook tab

step_1 = {
    "check": get_action_picture_by_name("skill_tab"),
    "verify": get_action_picture_by_name("spell"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_skill_tab"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_spell")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "select_skill_tab", 
}


# Step 2: Select Spell
step_1 = {
    "check": get_action_picture_by_name("placeholder"),
    "verify": get_action_picture_by_name("placeholder"),
    # add your own tests, however, no need because all the image icons should already be tested
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "use_spell", 
}

# final step, always add a final step, this is for the if else cases
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "object_markers_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}
 
def use_spell_steps(updates) -> list:
    action_ordered_steps = [step_0, step_1, final_step,]
    current_action_ordered_steps = copy.deepcopy(action_ordered_steps)
    return copy.deepcopy( update_action(current_action_ordered_steps, updates) )


def use_spell_by_id(spell_id):
    """
    must add all the spells here, add them by id
     spell id is the chosen spell id as indicated below
    """
    updates = [
        {
            "id": "use_spell",     
            "check": get_action_picture_by_name(f"all/dashboard/menu/spells/{spell_id}"),
            "verify": get_action_picture_by_name(f"all/dashboard/menu/spells/{spell_id}"),
            "verify_args": {
                "reverse_verification": True,
            },
        },
    ]
    return use_spell_steps(updates)


def apply_spell_on_target(target_id, spell_id):
    """
    this is for inventory targets, not for creature targets
     target_id is just the name of the item
    """
    spell_steps = use_spell_by_id(spell_id)
    spell_steps = [  step for step in spell_steps if step["id"] != "use_spell_final_step" ]
    # notice the _test usage here, if you want to test a specific item, you must name it properly
    try:
        test_image = get_test_picture_by_name(f"{target_id}_test")
        test_section = {
            "test": [
                {
                    "mock_image": test_image,
                    "replay_input": {"replay_type": "mouse", "coords": None},
                },
            ],
        }
    except Exception as e:
        test_section = {}
     
    spell_target_step = {
        "check": get_action_picture_by_name(target_id),
        "verify": get_action_picture_by_name("all/dashboard/menu/spells/magic_spell_cast_confirmation"),
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("all/dashboard/menu/spells/test/magic_spell_cast_confirmation_test"),
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "spell_target_step",
    }

    spell_target_step.update(test_section)
     
    final_step = {
        "check": none_step_verify,
        "verify": none_step_verify,
        "id": "spell_target_final_step",
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
    }
    return spell_steps + [ spell_target_step, final_step ]




# ONLY USED FOR action_tests.py
action_ordered_steps_test = apply_spell_on_target(target_id="adamant_platebody", spell_id="highalch")
