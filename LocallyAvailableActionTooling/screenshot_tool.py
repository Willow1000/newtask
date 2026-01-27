import base64
import threading
import os
import subprocess

import argparse
import mouse
import pyautogui
# from pynput import keyboard
# import keyboard

from screenshot_tool_lib import screenshot_tool_get_args
from screenshot_tool_lib import write_lines_to_file, read_lines_from_file, delete_any
from screenshot_tool_lib import create_unexisting_dir, copy_file
from screenshot_tool_lib import template_matching
from screenshot_tool_lib import load_image_from_file_to_bytes, \
    image_encode_to_send_to_network, \
    recreate_image_from_bytes


projects_path = "/opt/code/"


top_left = None
bottom_right = None
record_method = None
listener = None


def monitor_key_presses():
    # TODO actually not working to read keypresses from within the container
    # Start xev in a subprocess
    process = subprocess.Popen(['xev', '-root'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        while True:
            # Read output from xev line by line
            line = process.stdout.readline()
            if "state" in line and "keycode" in line:
                # Example key press output handling
                if 'LControl' in line:
                    print("Left Control key pressed.")
                    # perform_action()
                elif 'Escape' in line:
                    print("Escape key pressed. Exiting.")
                    break
    except KeyboardInterrupt:
        print("Process interrupted. Exiting.")
    finally:
        process.terminate()


def on_press(key):
    global top_left
    global bottom_right
    global listener
    # Example: Stop listener on pressing 'esc'
    # Check for left control and perform specific action
    print('testing on press')
    return
    if key == keyboard.Key.ctrl_l:
        print("Left Control Key pressed")
        top_left = pyautogui.position()
        if top_left is not None:
            if bottom_right is not None:
                # Stop the listener
                if listener:
                    print(f'top_left: {top_left}, bottom_right: {bottom_right}, stopped listener')
                    listener.stop()
                return
            bottom_right = pyautogui.position()


def get_position():
    global top_left
    global bottom_right
    global record_method
    
    if record_method is None:
        raise Exception("record method not set properly for some reason")
    elif record_method == "fullscreen":
        finalx, finaly = pyautogui.size()
        top_left = (1, 1)
        bottom_right = (finalx - 1, finaly - 1)
    elif record_method == "border":
        pos = pyautogui.position()
        print("position: " + str(pos))
        if top_left is None:
            top_left = pos
        elif bottom_right is None:
            bottom_right = pos


def onkeypress_get_pos(event):
    # waiting for events here doesn't work right
    global stop
    if event.name == 'ctrl' or event.name == "caps lock":
        get_position()


def wrapper_take_screenshot(template_match_image_to_test_photo_against, recording_method, 
                    screenshots_dir_per_action, file_name,
                    callback_type_str: str, coords=None):
    global top_left
    global bottom_right
    global record_method
    global listener
    # Create a listener
    # listener = keyboard.Listener(on_press=on_press, on_release=None)
    # Start the listener
    # listener.start()
    # listener.join()
    try:
        take_screenshot(template_match_image_to_test_photo_against, recording_method, 
                        screenshots_dir_per_action, file_name,
                        callback_type_str, coords=coords)
    except Exception as e:
        print()
        print("exception when trying to take screenshot, try again or quit")
        top_left = None
        bottom_right = None
        record_method = None
        # listener.stop()
        # listener.join()
        inp = input("enter the picture name(lowercase, no spaces), or q to quit: ")
        if inp.strip().lower() == "q":
            # Keep the program running to listen for events
            return False
        wrapper_take_screenshot(template_match_image_to_test_photo_against, recording_method, 
                                screenshots_dir_per_action, file_name,
                                callback_type_str, coords=coords)
    # Keep the program running to listen for events
    # listener.join()
    return True


def take_screenshot(template_match_image_to_test_photo_against, recording_method, 
                    screenshots_dir_per_action, file_name,
                    callback_type_str: str, coords=None):
    """
    screenshots_dir_per_action: screenshots/ directory within the action
    file_name: name of the file, not the path
    writes picture full path, top left coords and
     bottom right coords in log file, log file inside action
    """
    global top_left
    global bottom_right
    global record_method
    global listener
    
    record_method = recording_method
    
    is_using_keyboard = False
    if callback_type_str == "mouse_onclick":
        mouse.on_click(get_position)
    elif callback_type_str.startswith("keyboard"):
        # key = callback_type_str.split("_")[-1]
        # keyboard.on_press(onkeypress_get_pos) #  adding keyboard callbacks to events doesn't work properly without loading uinput modules, (must compile kernel again for that: # https://unix.stackexchange.com/questions/594470/wsl-2-does-not-have-lib-modules)
        is_using_keyboard = True
    elif callback_type_str == "coords":
        if coords is None:
            raise Exception("coords is None, must be non NULL")
        top_left = coords["top_left"]
        bottom_right = coords["bottom_right"]
    
    if is_using_keyboard:
        # listener.join()
        if top_left is None:
            print()
            inp = input("choose top left coords and press enter: ")
            if inp.strip().lower() == "q":
                exit()
            top_left = pyautogui.position()
        if bottom_right is None:
            print()
            inp = input("choose bottom right coords and press enter: ")
            if inp.strip().lower() == "q":
                exit()
            bottom_right = pyautogui.position()
    else:
        # waits for events that set top_left and top_right
        while top_left is None or bottom_right is None:
            continue
    
    screenshot_recursive(file_name, screenshots_dir_per_action, top_left, bottom_right)
    top_left = None
    bottom_right = None
    
    # template match check
    is_trying_again = False
    if template_match_image_to_test_photo_against is not None:
        path_of_image_to_find = screenshots_dir_per_action[0] + "/" + file_name  # any output path is fine, therefore, [0] index was chosen
        
        img_byte_array = load_image_from_file_to_bytes(template_match_image_to_test_photo_against)
        encoded_img = image_encode_to_send_to_network(img_byte_array)
        img_b64_str = encoded_img
        img_bytes = base64.b64decode(img_b64_str)
        
        print("comparing images from paths:")
        print(path_of_image_to_find)
        print(template_match_image_to_test_photo_against)
        base_image_obj = recreate_image_from_bytes(img_bytes)
        match_result_x, match_result_y, precision = template_matching(path_of_image_to_find, base_image_obj)
        match_result = (match_result_x, match_result_y)
        print()
        print("precision must be as high as possible")
        print("precision")
        print(precision)
        print("match_result")
        print(match_result)
        print()
        inp = input("try again?[y/N]: ")
        inp = inp.strip().lower()
        if inp == "y":
            is_trying_again = True
    return is_trying_again


def screenshot_recursive(file_name, screenshots_dir_per_action, top_left, bottom_right, cnt=0):
    try:
        screenshot(file_name, screenshots_dir_per_action, top_left, bottom_right)
    except Exception as e:
        cnt = cnt + 1
        if cnt > 3:
            print()
            print("exception when trying to take screenshot")
            print()
            raise e
        screenshot_recursive(file_name, screenshots_dir_per_action, top_left, bottom_right, cnt=cnt)


def screenshot(file_name, screenshots_dir_per_action, top_left, bottom_right):
    print("taking picture, file name: " + file_name)
    file_path_list = []
    for screenshots_path in screenshots_dir_per_action:
        create_unexisting_dir(screenshots_path)
        file_name_tokens = file_name.split("/")
        last_fn_token = file_name_tokens[-1]
        for token in file_name_tokens:
            if token == last_fn_token:
                break
            create_unexisting_dir(token)
        file_path_list.append(screenshots_path + "/" + file_name)
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]
    first_file_path = file_path_list[0]
    delete_any(first_file_path)
    pyautogui.screenshot(first_file_path, region=(top_left[0], top_left[1], width, height))
    for dest_file_path in file_path_list[1:]:
        delete_any(dest_file_path)
        copy_file(first_file_path, dest_file_path)
    
    coord_logs_path = screenshots_path + "/coord_logs.txt"
    try:
        new_lines = []
        lines = read_lines_from_file(coord_logs_path)
        # remove paths that already exist
        for original_line in lines:
            if original_line.startswith("#"):
                continue
            if original_line.strip() == "":
                continue
            parseled_line_list = original_line.split(" : ")
            line_path = parseled_line_list[0]
            if line_path in file_path_list:
                # replace (by deleting this lines and adding it again afterwards in next while loop)
                continue
            new_lines.append(original_line)
        lines = new_lines.copy()
    except Exception as e:
        lines = []
    
    for dest_file_path in file_path_list:
        line_to_write = dest_file_path + " : " + str(top_left) + " : " + str(bottom_right) + "\n"
        lines.append(line_to_write)
        write_lines_to_file(lines, coord_logs_path)
    

def run_screenshot_tool(coords, recording_method, callback_type_str, app_to_test, actions_to_put_images_in,
                        screenshot_file_name_list):
    actions_dir = projects_path + "/" + app_to_test + "/" + app_to_test + "/"
    screenshots_dir_per_action = []
    for current_action_to_test in actions_to_put_images_in:
        current_action_to_test_dir = actions_dir + current_action_to_test + "/all_action_files/screenshots/"
        print("actions_dir")
        print(actions_dir)
        screenshots_dir_per_action.append(current_action_to_test_dir)
    
    template_match_image_to_test_photo_against = None
    for screenshot_file_name in screenshot_file_name_list:
        while wrapper_take_screenshot(template_match_image_to_test_photo_against, recording_method, screenshots_dir_per_action, screenshot_file_name, callback_type_str, coords=coords):
            pass


def run_screenshot_tool_manually(template_match_image_to_test_photo_against_list, coords, recording_method,
                                 callback_type_str, screenshots_dir_per_action, screenshot_file_name_list):

    if screenshot_file_name_list:
        for i in range(len(screenshot_file_name_list)):
            screenshot_file_name = screenshot_file_name_list[i]
            if template_match_image_to_test_photo_against_list is None:
                template_match_image_to_test_photo_against = None
            else:
                template_match_image_to_test_photo_against = template_match_image_to_test_photo_against_list[i]
            print()
            print("screenshot_file_name base image:")
            print(screenshot_file_name)
            inp = input("c or enter to continue, q to stop taking pictures and quit\n")
            if inp.strip().lower() == "q":
                break
            while wrapper_take_screenshot(
              template_match_image_to_test_photo_against,
              recording_method,
              screenshots_dir_per_action,
              screenshot_file_name,
              callback_type_str,
              coords=coords,
            ):
                pass
    else:
        # thread = threading.Thread(target=monitor_key_presses)
        # thread.start()
        print('free picture mode')
        if template_match_image_to_test_photo_against_list is not  None: 
            for i in range(len(template_match_image_to_test_photo_against_list)):
                template_match_image_to_test_photo_against = template_match_image_to_test_photo_against_list[i]
                inp = input("enter the picture name(lowercase, no spaces): ")
                screenshot_file_name = inp.strip().lower()
                while wrapper_take_screenshot(template_match_image_to_test_photo_against, recording_method, screenshots_dir_per_action,
                                screenshot_file_name, callback_type_str,
                                coords=coords):
                    pass
        else:
            while True:
              template_match_image_to_test_photo_against = None
              inp = input("enter the picture name(lowercase, no spaces): ")
              screenshot_file_name = inp.strip().lower()
              while wrapper_take_screenshot(
                template_match_image_to_test_photo_against,
                recording_method,
                screenshots_dir_per_action,
                screenshot_file_name,
                callback_type_str,
                coords=coords,
              ):
                pass
             

def screenshot_tool_parse_arguments(args):
    coords = args.coords.strip().lower()
    if coords == "no":
        coords = None
    if coords is not None:
        coords_tuple = tuple(map(int, coords.split(',')))
        coords_dict = {
            "top_left": (coords_tuple[0], coords_tuple[1]),
            "bottom_right": (coords_tuple[2], coords_tuple[3])
        }
    else:
        coords_dict = None
    if args.template_match_image_to_test_photo_against_list is not None:
        template_match_image_to_test_photo_against_list = [k for k in args.template_match_image_to_test_photo_against_list.split(",")]
    else:
        template_match_image_to_test_photo_against_list = None
    recording_method = args.recording_method.strip().lower()
    callback_type_str = args.callback_type_str.strip().lower()
    app_to_test = args.app_to_test.strip().lower()
    actions_to_put_images_in = [k for k in args.actions_to_put_images_in.strip().lower().split(",")]
    if args.screenshot_file_name_list is not None: 
        screenshot_file_name_list = [k for k in args.screenshot_file_name_list.strip().lower().split(",")]
    else:
        screenshot_file_name_list = []
    return template_match_image_to_test_photo_against_list, coords_dict, recording_method, callback_type_str, app_to_test, actions_to_put_images_in, screenshot_file_name_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    screenshot_tool_get_args(parser)
    args = parser.parse_args()
    template_match_image_to_test_photo_against, coords, recording_method, callback_type_str, app_to_test, actions_to_put_images_in, screenshot_file_name_list = \
        screenshot_tool_parse_arguments(args)
    
    run_screenshot_tool(coords, recording_method, callback_type_str, app_to_test, actions_to_put_images_in, screenshot_file_name_list)

