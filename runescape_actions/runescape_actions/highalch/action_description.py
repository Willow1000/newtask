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
from runescape_actions.commons.use_spell.action_description import apply_spell_on_target 
# from runescape_actions.commons.definitions.full_setup import map_colors

all_failure_elements = {
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "highalch"
app_config_id = "initial-config"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



# from PIL import ImageGrab
# from PIL import Image
# import copy

# from common_action_framework.common_action_framework.basic_interaction import (
#     get_action_picture_by_name,
#     none_step_verify,
#     get_test_picture_by_name,
# )
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
# # )

# from common_action_framework.common_action_framework.reuse_action import (
#     update_action,
#     update_step,
#     merge_dicts,
# )


from runescape_actions.highalch_setup.action_description import setup,setup_without_withdraw
from runescape_actions.commons.withdraw_bank.action_description import get_withdraw_x
from runescape_actions.highalch_wrap_up.action_description import action_ordered_steps as wrap_up_steps, wrap_up_steps_without_deposit

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}



time_limit = None  # time limit for this action (in minutes)
current_action_id = "highalching"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



# check if firestaff is equiped
# click worn equipments



# setup
# def gen_setup_steps(item_id):
#     setup_steps = setup(item_id=item_id)
#     #TODO withdraw from the bank
#     return setup_steps

# def wrap_up_steps():
    
#     return wrap_up_steps    

 
def highalch_target_item(target_id):
    """
    target id is the item id
    """
    spell_steps = apply_spell_on_target(target_id, spell_id="highalch")
    return spell_steps 


def highalch_item(target_id):
    setup_steps = setup(target_id)
    spell_with_target_steps = highalch_target_item(target_id)
    # print(setup_steps,"then:\n\n")
    # print("swts",spell_with_target_steps)
    all_steps = setup_steps + spell_with_target_steps
    return all_steps

def jump_back_to_start(target_id):
    return [{
    "jump": {
        "step_num": "spell_target_step", 
        "verify": get_action_picture_by_name(target_id),
        "verify_mode": "verify_once",
        "reverse_verification": True,
       
    },
    "test": [
        {
            "mock_image": [get_test_picture_by_name(f"test_inventory_filled_with_{target_id}"),get_test_picture_by_name('test_items')],
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
        },
    ],
    "extra_test_info": {
        "loop_info": {
            "num_iterations": 1,
            "img_after_loop": get_test_picture_by_name(f"test_inventory_filled_with_{target_id}"),
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
        # "verify_args": [
        #     {
        #         "precision_required": 0.7,
               
        #     },
        # ],
    },
    "id": "high_alch_until_item_depletes",
    }]

# final step, always add a final step, this is for the if else cases
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "highalch_final_step",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

def get_action_ordered_steps(target_id):
    # setup_steps = gen_setup_steps(target_id)
    wrap_up = wrap_up_steps
    spell_with_target_steps = highalch_item(target_id)
    jump_back_to_start_steps = jump_back_to_start(target_id=target_id) #TODO add jump
    all_steps = spell_with_target_steps + jump_back_to_start_steps + wrap_up_steps + [final_step]
    return all_steps,target_id


# test item will be ALL items (only tests highalch for ALL, not setup, only tests setup ONCE)
# setup_item_id = "adamant_platebody"
# setup_steps_testing = gen_setup_steps(setup_item_id)
item_id_list = [
    "rune_platebody",
    "rune_kiteshield",
    "rune_longsword",
    "rune_pickaxe",
    "adamant_platebody",
    "rune_platelegs",
    "rune_full_helm",
    "rune_scimitar",
    "mithril_platebody",
    "rune_sq_shield",
    "rune_mace",
    "green_d'hide_body",
    "mithril_pickaxe",
    "rune_dagger",
    "adamant_med_helm",
    "rune_med_helm",
    "rune_plateskirt",
] # TODO add all the items and test (these are the items you are testing)



action_ordered_steps,item_id = get_action_ordered_steps("rune_longsword")

highalch_item = highalch_target_item(target_id = item_id)
# deposit_all_nature_rune =  deposit_all('nature_rune',"test_deposit_items")
# deposit_all_fire_staff =  deposit_all('fire_staff',"test_deposit_items")
withdraw_nature_rune = get_withdraw_x("30","nature_rune","test_withdraw_items")
withdraw_fire_staff = get_withdraw_x("1","fire_staff","test_withdraw_items")
withdraw_item = get_withdraw_x("26",item_id,f"test_withdraw_items")
custom_actions = setup_without_withdraw + wrap_up_steps_without_deposit

# action_ordered_steps_test = []
# action_ordered_steps_test += setup_steps_testing
# for item_id in item_id_list:
#     high_alch_steps_to_test = highalch_target_item(item_id)
#     action_ordered_steps_test += high_alch_steps_to_test
# action_ordered_steps_test += [final_step] 


