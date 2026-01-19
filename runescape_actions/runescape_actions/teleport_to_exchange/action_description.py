import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)

from common_action_framework.common_action_framework.common import (
    send_user_name_to_replay_in_client,
    send_pw_to_replay_in_client,
    send_delete_key_to_client,
    send_enter_key_to_client,
    send_tab_key_to_client,
    random_mouse_movement,
    verify_after_checking_once,
)

from runescape_actions.rs_login.action_logic.login_action_logic import (
    check_get_world_for_current_account,
    random_movement_for_check_world_step,
    get_world_verification_for_current_account,
)

"""
how does the action_ordered_steps format work?
 check RunningBotStatus class doc
"""
 
 
# so the thing about failure_elements is if you find a failure element on screen, then
# you go back to the step id given by the failure element's key, this is actually very useful,
# BUT, the failure element isnt actually an element to be add in the action, like verify,
# it's an element to be add in the failure_elements dict, and to be checked every few steps,
# actually it's better to check for them whenever there is a failure to see an image on
# screen, and that's how they get their name
# ideally there are barely any failure elements, because they are heavy on the processing side

# if one of failure element appears on screen, then: it goes to the step given by the id of that key
#  in this example, if the image "try_again_button" appears, then the action goes to the step with id "send_creds"
# the search for these failure_elements is only done whenever, the image in check is not found,
#  as it was supposed to be, only then the failure element search is triggered

all_failure_elements = {
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "teleport_to_exchange"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# TODO: add plugin warning window verifications (step 1 and 2 images)

# wait until app starts up
#  wait till service is in a state such that the action can start should always be step 0
step_0 = {
    "check": get_action_picture_by_name("spellbook_symbol"),
    "verify": get_action_picture_by_name("spellbook_symbol_pressed"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_before_pressing_spellbookj"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "replay_info": {
        "click_info": {
            "click_type": "click",
            "number_clicks": 1,
        },
    },
    "id": "press_spellbook_0",
}

step_1 = {
    "check": get_action_picture_by_name("varrock_teleport_symbol"), 
    "verify": get_action_picture_by_name("varrock_teleport_right_click_press_confirmation"), 
    "check_args": {
        "right_click": True
    },  
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_after_pressing_spellbook"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "replay_info": {
        "click_info": {
            "click_type": "click",
            "number_clicks": 1,
        },
    },
    "id": "varrock_teleport_right_click_1",
}

step_2 = {
    "check": random_movement_for_check_world_step,
    "union_to_next": True,
    "check_args": {
        "random_movement_for_check_world_step": {
            "wait_in_cli_secs": 1,
        },
    },
    "replay_info": {
        "click_info": {
            "click_type": "none",
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "random_movement_for_check_world_step_8",
}

step_3 = {
    "check": get_action_picture_by_name("press_grand_exchange_after_right_clicking_teleport_symbol"),
    "verify": get_action_picture_by_name("varrock_teleport_right_click_press_confirmation"),
    "verify_mode": "verify_once",
    "reverse_verification": True,
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_right_click_varrock_teleport"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "replay_info": {
        "click_info": {
            "click_type": "click",
            "number_clicks": 1,
        },
    },
    "id": "press_grand_exchange_after_right_clicking_teleport_symbol_3",
}

# TODO
#  step 2 is not done yet, it is a random movement, to make sure it is not highlighted, it should be a union step
#  step 4 is loop back to initial step, if the initial move To tile color is not found on screen
#  step 5 is moveTo grand exchange
step_4 = {
    "jump": {
        # a conditional jump, an if-else condition, in this case, representing a while loop between
        #  steps 6-10
        "step_num": 6,
        "verify": get_world_verification_for_current_account,
        "verify_mode": "verify_once",
        # verify_mode verify_once means that you only need to verify one of the images from the
        #  'verify' field list
        "reverse_verification": False,
        # "reverse_verification" reverses the condition required to verify the image (be careful because this will work together with verify_mode)
        #   it's the same as saying 'not verify get_world_verification_for_current_account'
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("ready_to_insert_password"),
            "replay_input": {
                # replay type of NA is because none of the input type matters in this case
                #  this is handled by not sending reply to server
                "replay_type": "NA",
                "word_to_write": None,
            },
            # reply_to_server set to False means no message will be sent to server to continue
            #  to the next step, this is used when you dont have to send anything to the server,
            #   for that specific test in that step, it's not exactly the same as not setting the
            #    'test' field
        },
    ],
    "extra_test_info": {
        # loop_info already handles 'end_mock_image' in a way
        # "end_mock_image_list": [ get_test_picture_by_name("password_inserted_screen") ],
        "loop_info": {
            "num_iterations": 1,
            "img_after_loop": get_test_picture_by_name("test_verify_world_308_pressed"),
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
        "verify_args": [
            # this is a list, because it's a set of args per verification image, and there can be more
            #  than one verification image, in this case, the corresponding element from this list
            #   to the image in the 'verify' field would the second element, because the failure
            #    elements count first in the verification step
            {
                # the default precision is 0.8, but you can change it here
                "precision_required": 0.9,
                #  due to this image being repeated (there is a bunch of ***),
                #  it's better to lower this precision because the template matching will not be so sure
                #   where to find the image, but since we want whatever repetition there may exist we can
                #    lower the precision and it will be fine, the idea is that
                #     a repeating image found will lower precision (obviously)
                #      this may become more apparent after testing, but usually you just want
                #       to use a different image, because a lower precision will mean the image repeats
            },
        ],
    },
    "id": "loop_until_world_selected_10",
}

# final step, always add a final step, this is for the if else cases
# final step should take a "test" field, this is because by default the previous step uses the next step "test" field to be able to test its steps
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "rs_login_final_step",
    "test": [
        {
        },
    ],
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
}

action_ordered_steps = [
    step_0,
    step_1,
    step_2,
    step_3,
    step_4,
    # always add final_step, this is for any need for an if-else statement
    final_step,
]


def get_teleport_to_exchange_test():
    # TODO
    return copy.deepcopy(action_ordered_steps)



