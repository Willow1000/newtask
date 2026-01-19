"""
purpose of this file: this file is meant to be have the api for all client functions 
 that can be used in the actions
since this is the common_action_framework, the functions here are meant to be used across 
 all apps
"""

import uuid
import time
import hashlib
import random

from common_action_framework.common_action_framework.image_matching_logic import (
    template_matching, image_b64_to_image_PIL_object, 
) 
from common_action_framework.common_action_framework.basic_interaction import (
    add_left_click_to_movement_request,
    add_right_click_to_movement_request,
    add_shift_right_click_to_movement_request,
    send_w,
    move_cursor_to_provided_image,
    request_mouse_action,
    add_click_type_to_movement_request,
)
from runelite_cv.runescape_cv.runescape_cv import (
    extract_objects,
) 


GLOBAL_VERIFICATION_MAP = {}  # kind of a wierd map only works for one thing, dont use this anywhere else

class StepManipulator:
    """
    class contains methods to manipulates step ids
     should also contain any methods to manipulate the action at setup time
    this class should always manipulate everything by reference
    """
    def __init__(self, 
                 action_ordered_steps, 
                 action_id,
                 app_config_id, 
                 context,
                 ):
        self.action_id = action_id
        self.app_config_id = app_config_id
        self.context = context
        self.action_ordered_steps = action_ordered_steps

    def initialize_step_ids(self):
        self.add_action_id_to_all_steps()
        self.add_numbers_to_step_ids()
        self.add_randomizer_to_step_id_all_steps()

    def add_action_id_to_step(self, step):
        step_id = step.get("id")
        new_step_id = f"{self.action_id}_{step_id}"
        step["id"] = new_step_id

    def add_action_id_to_all_steps(self):
        steps = self.action_ordered_steps
        for step in steps:
            self.add_action_id_to_step(step)
         
    def add_randomizer_to_step_id_all_steps(self):
        steps = self.action_ordered_steps
        for step in steps:
            self.add_randomizer_to_single_step_id(step)

    def add_randomizer_to_single_step_id(self, step):
        step_id = step.get("id")
        unique_id = f"{uuid.uuid4()}-{int(time.time())}"
        # Convert to a 6 letter string
        unique_id = hashlib.md5(unique_id.encode()).hexdigest()[:6]
        new_step_id = f"{step_id}_{unique_id}"
        step["id"] = new_step_id
     
    def add_numbers_to_step_ids(self):
        steps = self.action_ordered_steps
        for i in range(len(steps)):
            step = steps[i]
            step_number = i + 1
            self.add_number_to_step(step, step_number)

    def add_number_to_step(self, step, step_number):
        step_id = step.get("id")
        new_step_id = f"{step_id}_{step_number}"
        step["id"] = new_step_id
      

def get_common_args(args):
    """
    "reference_of_client_of_class"
    "input_from_previous_elements" is the payload (the dict with the cleaned input)
    """
    reference_of_client_of_class = args["reference_of_client_of_class"]
    input_from_previous_elements = args["input_from_previous_elements"]
    return reference_of_client_of_class, input_from_previous_elements


def send_user_name_to_replay_in_client(args):
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    profile = reference_of_client_of_class.get_profile()
    acc_name = profile.get_account_name()
    dict_to_ret = send_w(acc_name)
    return dict_to_ret
 
 
def send_pw_to_replay_in_client(args):
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    profile = reference_of_client_of_class.get_profile()
    pw = profile.get_account_password()
    dict_to_ret = send_w(pw)
    return dict_to_ret


def verify_after_checking_once(args):
    """
    the idea is it always needs to do the check at least one time before verifying
     but I want to do this in a way 
    """
    # another version of this in runningBotStatus
    global GLOBAL_VERIFICATION_MAP
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    client_id = reference_of_client_of_class.get_id()
    current_step_id = reference_of_client_of_class.get_running_bot_status().get_current_step_id()
    current_step = reference_of_client_of_class.get_running_bot_status().get_current_step()
    if current_step.get("jump", False):
        step_type = "jump"
    else: 
        step_type = "other"
    verification = GLOBAL_VERIFICATION_MAP.get(client_id, {}).get(current_step_id, {}).get("verification", False)
    ret_d = {
        "output_to_verification_step_bool": verification,
    }
    current_verification_map = GLOBAL_VERIFICATION_MAP.get(client_id, {})
    current_step_dict = current_verification_map.get(current_step_id, {}) 
    current_step_dict["verification"] = not verification
    current_step_dict["step_type"] = step_type
    current_verification_map[current_step_id] = current_step_dict
    GLOBAL_VERIFICATION_MAP[client_id] = current_verification_map
    return ret_d

 
def random_mouse_movement_aux(args, result_dict):
    """
    requirements:
        "msg_type" 
        "click_type" 
        "coords_type" 
        result_dict["coords"]
    """
    fn_args = args["args_by_func"]
    msg_type = fn_args["msg_type"]
    click_type = fn_args["click_type"]
    coords_type = fn_args["coords_type"]
    is_sending_to_movement_creation_processor = True 
     
    coords = result_dict["coords"]
    callback = coords

    callback_args = ()
    callback_kwargs = {}
    return request_mouse_action(msg_type, click_type, coords_type, is_sending_to_movement_creation_processor, callback, *callback_args, **callback_kwargs)


def random_mouse_movement(args, result_dict):
    '''
    this is just the movement, no click, all the defaults are no click
    requirements:
        "msg_type" 
        "click_type" 
        "coords_type" 
        result_dict["coords"]
    '''
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    coords = {
        "coords": {
            "xs": [random.randint(100, 600)], 
            "ys": [random.randint(100, 500)],
        },
        "replay_type": "mouse",
        "current_field_id": "check",
    }
    result_dict.update(coords)
    return random_mouse_movement_aux(args, result_dict)

 
def random_mouse_click(args):
    res_d = {}
    fn_args = args["args_by_func"]
    click_type = fn_args["click_type"]
    coords_type = fn_args["coords_type"]
    add_click_type_to_movement_request(fn_args, click_type, coords_type)
     
    out = random_mouse_movement(args, res_d)
    # out.update(movement_request_d)
    return out
     
     
def random_mouse_left_click(args):
    fn_args = args["args_by_func"]
    add_left_click_to_movement_request(fn_args)
    return random_mouse_click(args)


def random_mouse_right_click(args):
    fn_args = args["args_by_func"]
    add_right_click_to_movement_request(fn_args)
    return random_mouse_click(args)


def random_mouse_shift_right_click(args):
    fn_args = args["args_by_func"]
    add_shift_right_click_to_movement_request(fn_args)
    return random_mouse_click(args)
 
 
def client_wait(dict_to_add_ignore_info_to, seconds):
    """
    adds "cli_wait_secs" field, cli waits for the
     performed action on the client side before it sends the next image to the server, this is quite 
      useful in case you want to wait a couple seconds for an action to be performed on the client side without 
       sending the image back to the server, it may even optimize everything as the client will not 
        be sending any unnecessary images to the server if you do this correctly
     check reusable_actions/readme for more info
    """
    try:
        prev_time = dict_to_add_ignore_info_to["cli_wait_secs"]
    except KeyError as e:
        prev_time = 0
    new_time = prev_time + seconds
    dict_to_add_ignore_info_to.update(
        {
            "cli_wait_secs": new_time,
        }
    )


def click_image_by_click_type(args):
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    fn_args = args["args_by_func"]
    click_type = fn_args["click_type"]
    icon_image_path = fn_args["icon_image_path"]
    return move_cursor_to_provided_image(icon_image_path, click_type)


def left_click(args):
    '''
    requires: fn_args["icon_image_path"] 
    '''
    fn_args = args["args_by_func"]
    add_left_click_to_movement_request(fn_args)
    click_image_by_click_type(args)


def shift_right_click(args):
    '''
    requires: fn_args["icon_image_path"] 
    '''
    fn_args = args["args_by_func"]
    add_shift_right_click_to_movement_request(fn_args)
    click_image_by_click_type(args)


def right_click(args):
    '''
    requires: fn_args["icon_image_path"] 
    '''
    fn_args = args["args_by_func"]
    add_right_click_to_movement_request(fn_args)
    click_image_by_click_type(args)


def mouse_to_highlighted_area_movement(args):
    '''
    image: image object of the highlighted zone
    fn_args requires: click_type, coords_type, highlight_color
     input_from_previous_elements["img"] is the b64 image
     args['args_by_func']['highlight_color']
    '''
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    fn_args = args["args_by_func"]
    input_from_previous_elements = args["input_from_previous_elements"]
    current_func_args = fn_args["highlight_color"]
     
    color_list = current_func_args["highlight_color"]
    image = input_from_previous_elements["img"]
     
    # image is the image object, not the path
    callback = extract_objects
    callback_args = (image, color_list)
    callback_kwargs = {"add_debug_info": False}

    msg_type = fn_args["msg_type"]
    click_type = fn_args["click_type"]
    coords_type = fn_args["coords_type"]
     
    return request_mouse_action(msg_type, click_type, coords_type, 
        callback, *callback_args, **callback_kwargs)

 
def click_highlighted(args):
    '''
    clicks inside the highlighted zone
    '''
    fn_args = args["args_by_func"]
    click_type = fn_args["click_type"]
    coords_type = fn_args["coords_type"]
    out = mouse_to_highlighted_area_movement(args) 
    add_click_type_to_movement_request(out, click_type, coords_type)
    return out


def left_click_highlighted(args):
    '''
    requirements:
    input_from_previous_elements["img"] is the b64 image
    highlight_color: color of the boundaries of the highlighted zone 
    fn_args requires: template_match_for_step, highlight_color 
     template_match_for_step is a dict with the following fields: see template_match_for_step function  
    '''
    fn_args = args["args_by_func"]
    add_left_click_to_movement_request(fn_args)
    out = mouse_to_highlighted_area_movement(args)
    return out


def right_click_highlighted(args):
    fn_args = args["args_by_func"]
    add_right_click_to_movement_request(fn_args)
    out = mouse_to_highlighted_area_movement(args)
    return out


def shift_right_click_highlighted(args):
    fn_args = args["args_by_func"]
    add_shift_right_click_to_movement_request(fn_args)
    out = mouse_to_highlighted_area_movement(args)
    return out

def template_match_for_step_movement(args):
    """
    requires:
        fn_args["msg_type"]
        fn_args["click_type"] 
        fn_args["click_type"] 
    template_match_for_step is a dict with the following fields:
        image_to_find = current_func_args["image_to_find"]
        image_obj = input_from_previous_elements["img"]
        precision = current_func_args["precision"]
        offset = current_func_args["offset"]
    """
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    fn_args = args["args_by_func"]
    current_func_args = fn_args["template_match_for_step"]
    image_to_find = current_func_args["image_to_find"]
    image_b64 = input_from_previous_elements["img"]
    image_obj = image_b64_to_image_PIL_object(image_b64)
    # image_obj = current_func_args["image"]
    precision = current_func_args["precision"]
    try:
        offset = current_func_args["offset"]
    except KeyError as e:
        offset = (0, 0)
    # base_image must be PIL image 
    # ret_vals = template_matching(image_to_find, image_obj, precision, offset)
    # coords = (ret_vals[0], ret_vals[1])

    msg_type = fn_args["msg_type"]
    coords_type = fn_args["click_type"] 
    click_type = fn_args["click_type"] 
    return request_mouse_action(msg_type, coords_type, click_type, template_matching, 
                                image_to_find, image_obj, precision, offset, None)


def click_template_match_for_step_by_click_type(args):
    """
    requires:
    fn_args = args["args_by_func"]
    fn_args["msg_type"]
    fn_args["click_type"]
    fn_args["coords_type"]
    """ 
    fn_args = args["args_by_func"]
    fn_args["msg_type"] = "replay_input" 
    fn_args["click_type"] = "click"
    fn_args["coords_type"] = "singular"
    return template_match_for_step_movement(args)


def left_click_template_match_for_step_by_click_type(args):
    fn_args = args["args_by_func"]
    add_left_click_to_movement_request(fn_args)
    out = click_template_match_for_step_by_click_type(args)
    return out


def right_click_template_match_for_step_by_click_type(args):
    fn_args = args["args_by_func"]
    add_right_click_to_movement_request(fn_args)
    out = click_template_match_for_step_by_click_type(args)
    return out


def shift_right_click_template_match_for_step_by_click_type(args):
    fn_args = args["args_by_func"]
    add_shift_right_click_to_movement_request(fn_args)
    out = click_template_match_for_step_by_click_type(args)
    return out


def write_string_in_client(args):
    """
    write a string, if you want to write a number, you also use this, you cant really write numbers though
    """
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    fn_args = args["args_by_func"]
    current_func_args = fn_args["write_string_in_client"]
    name = current_func_args["string_to_write"]
    dict_to_ret = send_w(name)
    return dict_to_ret


def send_tab_key_to_client(args):
    # dont forget to add special keys into the word_commands list, xdotool file as an example: (keyboard_replay_xdotool.py)
    tab_key = "tab"
    dict_to_ret = send_w(tab_key)
    return dict_to_ret

 
def send_delete_key_to_client(args):
    # dont forget to add special keys into the word_commands list, xdotool file as an example: (keyboard_replay_xdotool.py)
    key = "del"
    dict_to_ret = send_w(key)
    return dict_to_ret


def send_enter_key_to_client(args):
    # dont forget to add special keys into the word_commands list, xdotool file as an example: (keyboard_replay_xdotool.py)
    enter_key = "enter"
    dict_to_ret = send_w(enter_key)
    return dict_to_ret


def format_name(input_string):
    return input_string.lower().replace(" ", "_")


