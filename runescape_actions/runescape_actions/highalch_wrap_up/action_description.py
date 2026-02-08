# from PIL import ImageGrab
# from PIL import Image
# import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
# from common_action_framework.common_action_framework.image_matching_logic import (
#     template_matching
# )
# from common_action_framework.common_action_framework.common import (
#     left_click_highlighted,
#     send_user_name_to_replay_in_client,
#     send_pw_to_replay_in_client,
#     send_tab_key_to_client,
#     send_enter_key_to_client,
#     random_mouse_movement,
#     verify_after_checking_once,
# )

# from common_action_framework.common_action_framework.reuse_action import (
#     update_action,
#     update_step,
#     merge_dicts,
# )

# from common_action_framework.common_action_framework.reuse_action import update_action
# from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
from runescape_actions.commons.deposit_bank.action_description import deposit_all
# from runescape_actions.commons.definitions.full_setup import map_colors

all_failure_elements = {

}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "highalching"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


# unequip firestaff
action_ordered_steps = []
def wrap_up():
    step_0 = {
        "check": get_action_picture_by_name("all/dashboard/menu/worn_equipment"),  
        "verify": [get_action_picture_by_name("all/dashboard/menu/worn_equipment_pressed")], 
        "verify_args": {
            "reverse_verification": True,
        }, 
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_worn_equipment"),  
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
    
        "replay_info": {
            "click_info": {
                "click_type": "click",
                "number_clicks": 1,
            },
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "check_fire_staff_equiped",
        }   
    step_1 = {
        "check": get_action_picture_by_name("fire_staff_equiped"),  
        "verify": [get_action_picture_by_name("fire_staff_unequiped")], 
        "verify_args": {
            "reverse_verification": True,
        }, 
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_fire_staff_equiped"),  
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "loop_info": {
                "num_iterations": 1,
                "img_after_loop": get_test_picture_by_name("test_fire_staff_unequiped"),
            },
        },
        "replay_info": {
            "click_info": {
                "click_type": "click",
                "number_clicks": 1,
            },
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "unequip_fire_staff",
    }

    action_ordered_steps += [step_0,step_1]

    items_to_be_deposited = ['nature_rune','fire_staff']


    for item in items_to_be_deposited:
        step = deposit_all(item,f"test_deposit_{item}")
        action_ordered_steps += step


    # final step, always add a final step, this is for the if else cases
    final_step = {
        "check": none_step_verify,
        "verify": none_step_verify,
        "id": "",
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
    }

    action_ordered_steps += [final_step]
    return action_ordered_steps


