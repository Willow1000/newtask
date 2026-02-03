from PIL import ImageGrab
from PIL import Image
import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.image_matching_logic import (
    template_matching
)
from common_action_framework.common_action_framework.common import (
    left_click_highlighted,
    send_user_name_to_replay_in_client,
    send_pw_to_replay_in_client,
    send_tab_key_to_client,
    send_enter_key_to_client,
    random_mouse_movement,
    verify_after_checking_once,
)

from common_action_framework.common_action_framework.reuse_action import (
    update_action,
    update_step,
    merge_dicts,
)

from common_action_framework.common_action_framework.reuse_action import update_action
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to
# from runescape_actions.commons.use_spell.action_description import action_ordered_steps as use_spell
from runescape_actions.commons.definitions.full_setup import map_colors

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "highalching_combat_bracelet_at_fountain_of_rune"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



# check if firestaff is equiped
# click worn equipments

# step_0 = {
#     "check": get_action_picture_by_name("all/dashboard/menu/worn_equipment"),  
#     "verify": [get_action_picture_by_name("all/dashboard/menu/worn_equipment_pressed"),get_action_picture_by_name("fire_staff")], 
#     "verify_args": {
#         "reverse_verification": True,
#     }, 
#     "test": [
#         {
#             "mock_image": get_test_picture_by_name("test_worn_equipment"),  
#             "replay_input": {"replay_type": "mouse", "coords": None},
#         },
#     ],
   
#      "replay_info": {
#         "click_info": {
#             "click_type": "click",
#             "number_clicks": 1,
#         },
#     },
#     "processor_info": {
#         "processor_type": {
#             "check": "template_match",
#             "verify": "template_match",
#         },
#     },
#     "id": "check_fire_staff_equiped",
# }

step_0 = {
    "check": get_action_picture_by_name("fire_staff"),  
    "verify": [get_action_picture_by_name("fire_staff")], 
    "verify_args": {
        "reverse_verification": True,
    }, 
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_fire_staff_equiped"),  
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
    "id": "equip_fire_staff",
}


step_1 = {
    "jump": {
        "step_num": "equip_fire_staff", 
        "verify": [get_action_picture_by_name("fire_staff_equiped")],
        "verify_mode": "verify_once",
        "reverse_verification": True,
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
            "img_after_loop": get_test_picture_by_name("test_spell"),
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
        "verify_args": [
            {
                "precision_required": 0.9,
            },
        ],
    },
    "id": "loop_until_firestaff_equiped",
}

# action_ordered_steps += [step_0,]
# updates = [
#     {
#         "id": "use_spell",     
#         "check": get_action_picture_by_name("high_alch"),
#         "verify": get_action_picture_by_name("rune_longsword"),
#         "verify_args": {
#             "reverse_verification": True,
#         },
#         "extra_test_info": {
#         "end_mock_image_list": [
#             get_test_picture_by_name("test_high_alch")
#         ],
#     },
#     },
# ]

# use_high_alch = copy.deepcopy( update_action(use_spell, updates) )
# step_
# action_ordered_steps +=  use_high_alch 


step_2 = {
    "check": get_action_picture_by_name("skill_tab"),
    "verify": [get_action_picture_by_name("spell")],
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_skill_tab"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "select_skill_tab", 
}


# Step 2: Select Spell

step_3 = {
    "check": get_action_picture_by_name("spell"),
    "verify": get_action_picture_by_name("rune_longsword"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_spell"),  
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_rune_longsword")
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "use_spell", 
}

step_4 = {
    "jump": {
        "step_num": "use_spell", 
        "verify": get_action_picture_by_name("rune_longsword"),
        "verify_mode": "verify_once",
        "reverse_verification": False,
       
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_rune_longsword"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "loop_info": {
            "num_iterations": 1,
            "img_after_loop": get_test_picture_by_name("test_inventory_without_rune_longsword"),
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
        "verify_args": [
            {
                "precision_required": 0.7,
               
            },
        ],
    },
    "id": "high_alch_until_item_depletes",
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

action_ordered_steps = [step_0, step_1,  step_2, step_3, final_step,]
highalching_nature_rune = [step_0, step_1,  step_2, step_3, final_step,]