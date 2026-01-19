import os
import random
import sys
import copy


"""
every function should accept a dictionary argument as input with all the arguments
functions can return other functions to serve as verification for the step they are on
"""

"""
specific functions only to be used in this action
"""
 
from common_action_framework.common_action_framework.common import (
    get_common_args,
    random_mouse_left_click,
    client_wait,
)
 
from common_action_framework.common_action_framework.basic_interaction import (
    ignore_processor,
) 

'''
when creating a new function, make sure you receive all your args in a dictionary, 
 this dictionary is the dictionary in the 'check_args' element (read more about in the 
  reusable_actions/README.md file, (file with all the elements)
 your 'check_args' or 'verify_args' elements is inside fn_args = args["args_by_func"] 
  you can see these in some of the functions below
'''


def random_movement_for_check_world_step(args):
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    fn_args = args["args_by_func"]
    current_func_args = fn_args["random_movement_for_check_world_step"]
    seconds_to_wait = current_func_args["wait_in_cli_secs"]
    result_dict = random_mouse_left_click(args)
    client_wait(result_dict, seconds_to_wait)
    ignore_processor(result_dict)
    return result_dict


def get_world_verification_for_current_account(args):
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    profile = reference_of_client_of_class.get_profile()
    world_name = profile.get_current_in_use_world()
    world_img_path = f"action/worlds/world_{world_name}_verification.png"
    image_to_find_path_list = [world_img_path]
    result_dict = {
        "image_to_find_path_list": image_to_find_path_list,
        "is_sending_to_processor": False,  # false, because only the string image_to_find_path_list goes to the processor, not this message
    }
    return result_dict

                                                                 
def pick_random_world_for_current_account_profile(profile):
    world_name_list = profile.get_worlds()
    if isinstance(world_name_list, str):
        world_name = world_name_list
    else:
        len_world_list = len(world_name_list)
        max_index_world_list = len_world_list - 1
        max_rand_num = max_index_world_list
        r_int = random.randint(0, max_rand_num)
        world_name = world_name_list[r_int]
    profile.set_current_in_use_world(world_name)
    return world_name


def check_get_world_for_current_account(args):
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    profile = reference_of_client_of_class.get_profile()
    world_name = pick_random_world_for_current_account_profile(profile)
    world_img_path = f"action/worlds/world_{world_name}.png"
    image_to_find_path_list = [world_img_path]
    # TODO crop image and send off to processor
    # next_step_num = reference_of_client_of_class.get_running_bot_status().get_current_step_num() + 1
    result_dict = {
        "image_to_find_path_list": image_to_find_path_list,
        "is_sending_to_processor": False,  # false, because only the string image_to_find_path_list goes to the processor, not this message
    }
    return result_dict


