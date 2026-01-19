import random

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
    StepManipulator,
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

# num_required_clients is the number of clients required to run this action (feature required for tests)
import copy

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
    "send_creds": [
        # for example this failure element is meant to be checked in case the step_11 fails
        # so, after step_12 fails, the system will look for this image, and go back to step_11
        # this is not meant to be used instead of a while loop, in this case this is used as an example,
        # but, a while loop as shown in the commented step_12 would have been better in this case
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "rs_login"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.

# TODO: add plugin warning window verifications (step 1 and 2 images)

# wait until app starts up
#  wait till service is in a state such that the action can start should always be step 0
step_0 = {
    "check": none_step_verify,
    "verify": [ 
        get_action_picture_by_name("rs_app_started"),
        get_action_picture_by_name("welcome_to_runescape_message_in_initial_login_menu"),
        get_action_picture_by_name("existing_user"), 
        get_action_picture_by_name("terms_of_service"),
        get_action_picture_by_name("accept_terms"),
    ],
    "verify_mode": "verify_once",
    "test": [
        {
            "mock_image": get_test_picture_by_name("initial_screen_for_rs_app_didnt_appear_yet"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_existing_user"),
            get_test_picture_by_name("rs_app_requires_update"),
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "wait_for_app_to_startup",
}

# TODO: unfinished: check if update is required
#  check must be a function that warns me about the update to my discord app
step_1 = {
    "check": none_step_verify, # TODO the check or verify step has to verify and send exception that updates and restarts app in client side (image name to verify is: update_app_verification) (this is that annoying message that keeps poping up to update client to newest version), make sure you update the previous message you previously sent, if any is in memory
    "verify": none_step_verify,
    "test": [
        {
            "mock_image": get_test_picture_by_name("rs_app_requires_update"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_existing_user"),
            get_test_picture_by_name("rs_app_requires_update"),
        ],
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "verify_if_rs_app_requires_update",
}

# this is meant to be repeated with step 4
step_2 = {
    "check": get_action_picture_by_name("terms_of_service"),
    "verify": get_action_picture_by_name("terms_of_service"), 
    "reverse_verification": True,
    "test": [
        {
            "mock_image": get_test_picture_by_name("terms_of_service_test_screen"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [get_test_picture_by_name("test_existing_user")],
    },
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
    "id": "accepts_terms_of_service",
    "error_limit": None,
}

step_3 = {
    "check": get_action_picture_by_name("plugin_warning_msg"),
    "verify": get_action_picture_by_name("plugin_warning_msg"), 
    "reverse_verification": True,
    "extra_test_info": {
        "end_mock_image_list": [get_test_picture_by_name("test_existing_user")],
    },
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
    "id": "warning_msg",
    "error_limit": None,
}

step_3_5 = {
    "check": get_action_picture_by_name("OK_button_for_unable_to_open_link_message"),
    "verify": [get_action_picture_by_name("OK_button_for_unable_to_open_link_message")],
    # need the accept_terms_test_screen image to be added to the test images
    "reverse_verification": True,
    "test": [
        {
            "mock_image": get_test_picture_by_name("press_ok_and_the_link_will_be_copied_after_loign_screen"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "verify_mode": "verify_once",
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
    "id": "unable_to_open_link_message",
    "error_limit": None,
}

step_4 = {
    "check": get_action_picture_by_name("accept_terms"),
    "verify": [get_action_picture_by_name("existing_user")],
    # need the accept_terms_test_screen image to be added to the test images
    "test": [
        {
            "mock_image": get_test_picture_by_name("terms_of_service_test_screen"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [get_test_picture_by_name("test_existing_user")],
    },
    "verify_mode": "verify_once",
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
    "id": "accepts_terms_of_service",
    "error_limit": None,
}

step_4_5 = {
    "check": get_action_picture_by_name("OK_button_for_unable_to_open_link_message"),
    "verify": [get_action_picture_by_name("OK_button_for_unable_to_open_link_message")],
    # need the accept_terms_test_screen image to be added to the test images
    "reverse_verification": True,
    "test": [
        {
            "mock_image": get_test_picture_by_name("press_ok_and_the_link_will_be_copied_after_loign_screen"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "verify_mode": "verify_once",
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
    "id": "unable_to_open_link_message",
    "error_limit": None,
}

step_5 = {
    "check": get_action_picture_by_name("existing_user"),
    "verify": get_action_picture_by_name("existing_user_btn_press_confirmation"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_existing_user"),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [
            get_test_picture_by_name("test_change_world_main_screen_with_change_world_button")
        ],
    },
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
    "id": "press_existing_user",
}

# steps 6 through 10 is a while loop
# if you notice the debug logs for the images of step 6 you notice an extra image, after the first
# loop, this is because of step 10's jump
# step_10's jump field does a verify to know where to jump to followed by a check,
# that second check is a check for the step it jumps to, this is actually fine,
# you get to see if the step it's jumping to is correct
step_6 = {
    "check": get_action_picture_by_name("change_world"),
    "check1": get_action_picture_by_name("change_world_2"),
    "verify": get_action_picture_by_name("change_world_confirm"),
    "test": [
        {
            "mock_image": get_test_picture_by_name(
                "test_change_world_main_screen_with_change_world_button"
            ),
            "replay_input": {"replay_type": "mouse", "coords": None},
        },
    ],
    "extra_test_info": {
        "end_mock_image_list": [get_test_picture_by_name("screen_with_all_worlds")],
    },
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
    "id": "change_world",
}

# find_image_in_worlds, but don't send back to client,
#  such that step_9 uses the info found and uses it
# check_get_world_for_current_account, picks the in-use world, which will be used in steps 7-10
#  step 7 through 9 are all required, it has to do with moving the mouse out of the way, to avoid changing the icon to press(hovering the icon will highlight it)
step_7 = {
    "check": check_get_world_for_current_account,
    "verify": verify_after_checking_once,
    "info_for_step": {
        "send_back_to_cli": False,
        "is_waiting_for_cli_to_proceed": False,
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("screen_with_all_worlds"),
            "replay_input": {
                "replay_type": "mouse",
                "coords": None,
            },
        },
    ],
    # end_mock_image doesnt make sense here
    # "extra_test_info": {
    # "end_mock_image_list": [ get_test_picture_by_name("test_existing_user") ],
    # },
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
    "id": "find_image_in_worlds",
}

# step 8 is just meant to move the mouse around randomly, and then instantly execute step 9,
#  this is done this way to avoid changing the image onscreen with highlights
#   if there was only step 9, the check element would have to be a list and sometimes this
#    is way more cleaner and easier to understand, cleaner code I suppose
#     this way the 'check_args' is way more clean, that is mostly what the union_to_next is for
step_8 = {
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
    "id": "random_movement_for_check_world_step",
}

# explaining step 9 logs a bit:
# step 9 should have the 2 extra images, because it's the union of the check from step 8
#  AND the following verify->check combo: ex.: check(step8), verify(step9), check(step9)
#   AND this is for the step 8 resolution, afterwards, there are 3 more, therefore, there
#    are 5 images in an union step
step_9 = {
    "check": check_get_world_for_current_account,
    "verify": get_action_picture_by_name("existing_user_btn_press_confirmation"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("screen_with_all_worlds"),
            "replay_input": {
                "replay_type": "mouse",
                "coords": None,
            },
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
    "id": "press_chosen_world_btn",
}

# step 10 logs explained: since step 10 is a loop, AND the verify step only happens for the last
# iteration in the loop, you only see one image
# while loop done with jump
step_10 = {
    "jump": {
        # a conditional jump, an if-else condition, in this case, representing a while loop between the current step and "step_num"
        # (it jumps if the condition in verify is false)
        "step_num": "change_world", 
        "verify": get_world_verification_for_current_account,
        "verify_mode": "verify_once",
        # verify_mode verify_once means that you only need to verify one of the images from the
        #  'verify' field list
        "reverse_verification": False,
        # "reverse_verification" reverses the condition required to verify the image (BEWARE: this will work together with verify_mode)
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
    "id": "loop_until_world_selected",
}

step_11 = {
    "check": get_action_picture_by_name("inside_login_menu_login_button_to_insert_username"),
    "verify": verify_after_checking_once,
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
    "id": "press_insert_username",
}

step_12 = {
    "check": 
    [ send_delete_key_to_client ] * (40 + random.randint(0, 5)) + \
    [
        send_user_name_to_replay_in_client,
        send_tab_key_to_client,
    ] + \
    [ send_delete_key_to_client ] * (40 + random.randint(0, 5)) + \
    [
        send_pw_to_replay_in_client,
        send_enter_key_to_client,
    ],
    "verify": verify_after_checking_once,
    "test": [
        {
            "mock_image": get_test_picture_by_name("ready_to_insert_password"),
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
        },
    ],
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        },
        "verify_args": [
            # this is a list, because it's a set of args per verification image, and there can be more
            #  than one verification image, in this case, the corresponding element from this list
            #   to the image in the 'verify' field would the second element, because the failure
            #    elements count first in the verification step
            {
                # the default precision is 0.8, but you can change it here
                "precision_required": 0.65,
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
    "id": "send_creds",
}

# must wait because a jump step instantly jumps if the UI hasnt updated accordingly (ignoring the if clause)
#  a common example of awaiting until the image exists and then using the image in a decision
step_12_2 = {
    "check": none_step_verify,
    "verify": [
        get_action_picture_by_name("try_again_button"),
        get_action_picture_by_name("click_here_to_play_button"),
        get_action_picture_by_name("inventory"),
    ],
    "verify_mode": "verify_once",
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "await_by_verify_on_all_images_a_change_in_UI_is_verified_before_making_jump_decision",
}

step_13 = {
    "jump": {
        # (it jumps if the condition in verify is false)
        "step_num": "enter_game",
        "verify": [
            get_action_picture_by_name("click_here_to_play_button"),
            get_action_picture_by_name("inventory"),
        ],
        "verify_mode": "verify_once",
        "reverse_verification": True,
    },
    "test": [
        {
            "mock_image": get_test_picture_by_name("try_again_screen"),
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
        "loop_info": {
            "num_iterations": 2,
            "img_after_loop": get_test_picture_by_name("test_login_success"),
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "loop_until_login_successful",
}

step_14 = {
    "check": get_action_picture_by_name("try_again_button"),
    "verify": get_action_picture_by_name("existing_user"),
    "test": [
        {
            "mock_image": get_test_picture_by_name("try_again_screen"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
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
    "id": "try_again_handling",
}

step_15 = step_5
step_15["id"] = "press_existing_user_after_try_again"

# go to password input field
step_16 = {
    "check": get_action_picture_by_name("inside_login_menu_password_button"),
    "verify": verify_after_checking_once,
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_change_world_main_screen_with_change_world_button"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
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
    "id": "select_password_field_for_password_insertion",
}

# delete only pw, because when existing user is pressed you automatically go to the password field
step_17 = {
    "check":
    [ send_delete_key_to_client ] * (40 + random.randint(0, 5)) + [ send_pw_to_replay_in_client ],
    "verify": verify_after_checking_once,
    "check_args": {
        "num_deletes": 20,
    },  
    "replay_info": {
        "click_info": {
            "click_type": "click",
            "number_clicks": 1,
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        },
    },
    "id": "delete_and_reinsert_pw",
}

step_18 = {
    "check": get_action_picture_by_name("inside_login_menu_login_button_to_insert_username"),
    "verify": verify_after_checking_once,
    "test": [
        {
            "mock_image": get_test_picture_by_name("password_inserted_screen"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
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
    "id": "select_username_field_for_username_insertion",
}

# insert username
step_19 = {
    "check":
    [ send_delete_key_to_client ] * (40 + random.randint(0, 5)) + \
    [ send_user_name_to_replay_in_client],
    "verify": verify_after_checking_once,
    "processor_info": {
        "processor_type": {
            "check": "xdot_keyboard_processing",
            "verify": "template_match",
        },
    },
    "id": "delete_and_reinsert_username",
} 

step_20 = {
    "jump": {
        "step_num": "loop_until_world_selected", 
        "verify": none_step_verify,  # always true, it's a jump, not a conditional jump
        "verify_mode": "verify_once",
        "reverse_verification": True,
    },
    "extra_test_info": {
        "loop_info": {
            "num_iterations": 1,
            "img_after_loop": get_test_picture_by_name("test_change_world_main_screen_with_change_world_button"),
        },
    },
    "processor_info": {
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
    },
    "id": "loop_to_retry_login",
}

step_21 = {
    "check": get_action_picture_by_name("unable_to_open_link_ok_button"),
    "verify": get_action_picture_by_name("unable_to_open_link_ok_button"),
    "reverse_verification": True,
    "test": [
        {
            "mock_image": get_test_picture_by_name("press_ok_and_the_link_will_be_copied_after_loign_screen"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
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
    "id": "occasional_unable_to_open_link_ok_button",
}

# login (actually enters the game)
step_22 = {
    "check": get_action_picture_by_name("click_here_to_play_button"),
    "verify": [ get_action_picture_by_name("inventory"), get_action_picture_by_name("inventory_pressed") ],
    "verify_mode": "verify_once",
    "test": [
        # {
            # I set this one in the next step, for verify, instead of setting it here
            # "mock_image": get_test_picture_by_name("test_login_success"),
            # "replay_input": {
                # "replay_type": "keyboard",
                # "word_to_write": None,
            # },
        # },
        {
            "mock_image": get_test_picture_by_name("pre_login_screen"),
            "replay_input": {
                "replay_type": "NA",
                "word_to_write": None,
            },
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
    "id": "enter_game",
}

# final step, always add a final step, this is for the if else cases
# final step should take a "test" field, this is because by default the previous step uses the next step "test" field to be able to test its steps
final_step = {
    "check": none_step_verify,
    "verify": none_step_verify,
    "id": "rs_login_final_step",
    "test": [
        {
            "mock_image": get_test_picture_by_name("test_login_success"),
            "replay_input": {
                "replay_type": "keyboard",
                "word_to_write": None,
            },
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
    step_3_5, # step_3_5 and step_4_5 are the same on purpose 
    step_4,
    step_4_5, # step_3_5 and step_4_5 are the same on purpose
    step_5,
    step_6,
    step_7,
    step_8,
    step_9,
    step_10,
    step_11,
    step_12,
    step_12_2,
    step_13,
    step_14,
    step_15,
    step_16,
    step_17,
    step_18,
    step_19,
    step_20,
    step_21,
    step_22, 
    # always add final_step, this is for any need for an if-else statement
    final_step,
]

StepManipulator(
    action_ordered_steps, 
    current_action_id,
    app_config_id,
    context,
).initialize_step_ids()


