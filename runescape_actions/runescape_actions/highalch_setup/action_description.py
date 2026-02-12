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

# # from common_action_framework.common_action_framework.reuse_action import (
# #     update_action,
# #     update_step,
# #     merge_dicts,
# )

# from common_action_framework.common_action_framework.reuse_action import update_action
# from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
# from runescape_actions.commons.use_spell.action_description import use_spell_action
# from runescape_actions.commons.definitions.full_setup import map_colors
from runescape_actions.commons.withdraw_bank.action_description import get_withdraw_x

all_failure_elements = {
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "highalching"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

step_1 = {
    "check": get_action_picture_by_name("fire_staff"),  
    "verify": [get_action_picture_by_name("fire_staff_equiped")], 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_fire_staff"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "loop_info": {
            "num_iterations": 1,
            "img_after_loop": get_test_picture_by_name("test_fire_staff_equiped"),
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
    "id": "equip_fire_staff",
}

step_2 = {
    "check": get_action_picture_by_name("all/dashboard/menu/worn_equipment"),  
    "verify": [get_action_picture_by_name("all/dashboard/menu/worn_equipment_pressed"),get_action_picture_by_name("fire_staff_equiped")], 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("all/dashboard/menu/test_worn_equipment"),  
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

step_3 = {
    "jump": {
        "step_num": "equip_fire_staff", 
        "verify": [get_action_picture_by_name("fire_staff_equiped")],
        "verify_mode": "verify_once",
        "reverse_verification": False,
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_fire_staff_equiped"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "loop_info": {
            "num_iterations": 1,
            "img_after_loop": get_test_picture_by_name("test_fire_staff_equiped"),
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
        # "verify_args": [
        #     {
        #         "precision_required": 0.9,
        #     },
        # ],
    },
    "id": "loop_until_firestaff_equiped",
}

final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "highalch_setup_final",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

setup_without_withdraw = [step_1, step_2, step_3]

def setup(item_id):
    action_ordered_steps = []
    items_to_be_withdrawn = ['nature_rune','fire_staff',item_id]
    item_quantity_dict = {
        "nature_rune": 30,
        "fire_staff": 1,
        item_id: 26
    }
    for item in items_to_be_withdrawn:
        action_ordered_steps+= get_withdraw_x(item_quantity_dict.get(item),item,f"test_withdraw_items")

    action_ordered_steps += [step_1,step_2,step_3,final_step]
    return action_ordered_steps



