import os 
import sys 
import inspect
import time

'''
this file is the interaction functions for the client, these are all the functions 
 that perform some sort of action on the client
these functions here will then be used in the commons.py (the api for all client functions)
to not clog commons.py too much, this file contains the basic building blocks for more complex behavior, that more 
 complex behavior is in commons.py
''' 
 
 
def request_mouse_action(
    msg_type,
    click_type,
    coords_type,
    is_sending_to_movement_creation_processor,
    coords_callback,
    *callback_args,
    **callback_kwargs,
):
    """
    "msg_type": this is the type of message being sent back to the client after it is "processed", 
     here we are simulating that message type, it will usually be "replay_input"
    "click_type": this click_type will be used to set if this click is a: left, right, shift_right
     or whatever type of click there is
    "coords_type": will set for what these coords are used for, because the coords can be in 
     any format, coords type will help to know how to interpret these
    "is_sending_to_movement_creation_processor": this bool will set if this request is sent 
     to the movement creation processor, this is just the target, the output of the coords callback 
      is just the final destination of the movement, the whole movement creation processor will add 
       the remaining movement in between the points
    this function will accept a callback function and its args, this coords_callback 
     funtion is basically a custom processor, can also process the movement
    coords_callback: function that will return the coords to click at, or the a dictionary with the coords
      if the coords are the coordinates and not a function, it just accepts the coords
       these coords must be in the format:
          coords = {
              "coords": {
                  "xs": [random.randint(100, 600)], 
                  "ys": [random.randint(100, 500)],
              },
              "replay_type": "mouse",
              "current_field_id": "check",
          }
    callback_args: is a list of args that will be fed to the coords_callback, will 
      always contain the image from client though, this is because this is essentially  custom processor
    requires: msg_type, click_type, coords_type, 
     coords_callback, callback_args 
    return: dict with everything setup to send to the movement processor
    """
    if isinstance(coords_callback, dict):
        coords = coords_callback
    else:
        coords = coords_callback(*callback_args, **callback_kwargs)
    dict_to_ret = {
        "msg_type": msg_type,
        "replay_type": "mouse",
        "click_type": click_type,
        "is_sending_to_movement_creation_processor": is_sending_to_movement_creation_processor,
        "coords_type": coords_type,
        "coords": coords,
        "is_sending_to_processor": False,
    }
    return dict_to_ret

 
def add_click_type_to_movement_request(movement_request_dict, click_type, coords_type):
    '''
    :movement_request_dict: dict with all the movement request (ex: received from request_mouse_action)
    :click_type this function will add a click to the movement request dict
    returns the modified dict
    '''
    movement_request_dict["msg_type"] = "replay_input" 
    movement_request_dict["click_type"] = click_type
    movement_request_dict["coords_type"] = coords_type
    return movement_request_dict


def add_left_click_to_movement_request(movement_request_dict):
    click_type = "left"
    coords_type = movement_request_dict.get( "coords_type", "singular" ) 
    return add_click_type_to_movement_request(movement_request_dict, click_type, coords_type)

 
def add_right_click_to_movement_request(movement_request_dict):
    click_type = "right"
    coords_type = movement_request_dict.get( "coords_type", "singular" ) 
    return add_click_type_to_movement_request(movement_request_dict, click_type, coords_type)


def add_shift_right_click_to_movement_request(movement_request_dict):
    click_type = "shift_right"
    coords_type = movement_request_dict.get( "coords_type", "singular" ) 
    return add_click_type_to_movement_request(movement_request_dict, click_type, coords_type)


def move_cursor_to_provided_image(image_path, click_type):
    '''
    image_path: path of the icon image (provided image)
    click_type: type of click to perform (left, right, shift_right, etc)
    this is meant to be sent to processor
    '''
    msg_type = "replay_input"
    coords_type = "singular" # singular means that the coords are a single point
    image = cv2.imread(image_path)

    # coords are not represented cause it's a singular point
    is_sending_to_movement_creation_processor = True
    return {
        "msg_type": msg_type,
        "replay_type": "mouse",
        "click_type": click_type,
        "is_sending_to_movement_creation_processor": is_sending_to_movement_creation_processor,
        "coords_type": coords_type, 
        "image": image, 
        "is_sending_to_processor": True,
    }

 
def send_w(word_to_write):
    """
    input: word
    returns dict with everything setup to send the
     received string to replayed on the client's
      keyboard
    """
    msg_type = "replay_input"
    return {
        "msg_type": msg_type,
        "replay_type": "keyboard",
        "word_to_write": word_to_write,
        "is_sending_to_processor": True,  # still goes to processor (depending on the processor the output string may be very different)
    }


def none_step_verify(args):
    """
    this does nothing, not meant to be a placeholder, only meant to do nothing
    return: purpose is to do nothing
    """
    return {
        "output_to_verification_step_bool": True,
        # "send_back_to_cli": False,  # if this is in verify step, if used, it would never go back to client, not even the check's output
        "is_sending_to_processor": False,  # still goes to processor (depending on the processor the output string may be very different)
    }


def always_fail_verify(args):
    return {
        "output_to_verification_step_bool": False,
        "is_sending_to_processor": False,  # still goes to processor (depending on the processor the output string may be very different)
    }


def get_sleep_step(check_args, verify_conditions: dict):
    """
    this step will make the client sleep for a certain amount of time
    args: args should contain the time to sleep in seconds
    """
    out = {
        "check": sleep,
        "check_args": check_args,
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "sleep_step",
    }
    out.update(verify_conditions)
    return out


def sleep(args):
    fn_args = args["args_by_func"]
    time_in_seconds_range = fn_args["sleep_seconds_range"]
    time_in_seconds = int.from_bytes(os.urandom(2), 'big') % (time_in_seconds_range[1] - time_in_seconds_range[0] + 1) + time_in_seconds_range[0]
    time.sleep(time_in_seconds)
    return {
        "is_sending_to_processor": False,  # still goes to processor (depending on the processor the output string may be very different)
    }


def get_picture_by_name(prepend, name):
    if name.startswith("all/"):
        prepend = "all"
        name = name[4:]
    else:
        prepend = prepend.strip().lower()
        name = name.strip().lower()
    out_path = f"{ prepend }/{ name }.png"
    return out_path 


def get_action_picture_by_name(name):
    prepend = "action"
    return get_picture_by_name(prepend, name)


def get_test_picture_by_name(name):
    prepend = "test"
    return get_picture_by_name(prepend, name)


def ignore_processor(dict_to_add_ignore_info_to):
    """
    adds fields to ignore the processor
    """
    dict_to_add_ignore_info_to.update(
        {
            "is_sending_to_processor": False,
            "send_back_to_cli": True,
        }
    )


def ignore_client(dict_to_add_ignore_info_to):
    """
    doesn't send msg back to client
    so what does this mean?
     the client sends a message with the screen back to the server, when it receives a message from the server 
      OR every X seconds, if you set this to False, you dont send a message back from the server to the client, so you WILL 
       have to wait the X seconds, which tends to be unwanted, so be careful when using this
    you may want to use: ignore_client_but_respond
    """
    dict_to_add_ignore_info_to.update(
        {
            "send_back_to_cli": False,
        }
    )


def ignore_client_but_respond(dict_to_add_ignore_info_to):
    """
    instead of just ignoring client and waiting X seconds for client to send back the next image, this 
     just sends a response to the client, the client will ignore it and not replay any inputs, but the 
      client will respond right away, which is ideal in most cases
    """
    dict_to_add_ignore_info_to.update(
        {
            "send_back_to_cli": True,
            "send_blank_response_to_cli": True,
        }
    )
     



