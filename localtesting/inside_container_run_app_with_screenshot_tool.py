import os
import sys
import threading
import time

import Xlib
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay

projects_path = "/opt/code/"

def find_screenshot_dirs_per_action(is_testing_in_cli, app_to_test, actions_to_put_images_in):
    if not is_testing_in_cli:
        actions_dir = projects_path + "/" + app_to_test + "/" + app_to_test + "/"
        screenshots_dir_per_action = []
        for current_action_to_test in actions_to_put_images_in:
            current_action_to_test_dir = actions_dir + current_action_to_test + "/all_action_files/screenshots/"
            screenshots_dir_per_action.append(current_action_to_test_dir)
    else:
        screenshots_dir_per_action = ["/opt/data/photos"]
    return screenshots_dir_per_action
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--running_command",
                        help="string of the full command running the app",
                        default=True)
    parser.add_argument("--run_screenshot_tool_thread",
                        help="[y/n] required to know if the screenshot tool is running within the container or not",
                        required=True)
    parser.add_argument("--x_axis_size",
                        help="x axis size of screen",
                        default=1024)
    parser.add_argument("--y_axis_size",
                        help="y axis size of screen",
                        default=768)
    # screen size in: display_config

    try:
        os.environ["TESTING_IN_CLIENT"]  # must be set containers other than cent man.
        is_testing_in_cli = True
    except KeyError as e:
        is_testing_in_cli = False

    from screenshot_tool_lib import screenshot_tool_get_args

    screenshot_tool_get_args(parser)
    args = parser.parse_args()
    running_command = args.running_command.strip()
    
    run_screenshot_tool_thread = args.run_screenshot_tool_thread.strip().lower()
    is_running_screenshot_tool_in_thread = False
    if run_screenshot_tool_thread == "y":
        is_running_screenshot_tool_in_thread = True

    print()
    display_env_var = os.environ["DISPLAY"] 
    print("display: " + str(display_env_var))
    custom_env = {
        'OUTSIDE_DISPLAY': display_env_var,
    }
    # running_command = f'export DISPLAY={disp}; { running_command }'
    print()
    print("running_command: ")
    print(running_command)

    x_axis_size = args.x_axis_size
    y_axis_size = args.y_axis_size
    with SmartDisplay(visible=1, size=(x_axis_size, y_axis_size)) as disp:
        import pyautogui
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])
        # os.environ["DISPLAY"] = display_env_var
        finalx, finaly = pyautogui.size()
        print("screen size, x: " + str(finalx) + " y: " + str(finaly))
        # os.system("xrandr | fgrep '*'")  # this is used to test if the real display size is correct
        # print()
        try:
            # with EasyProcess(running_command, env=custom_env) as app_process:
                # setting a new display with env=custom_env wont work to redirect the keyboard 
                 # to the display, the keyboard will still be redirected to the host machine, it doesnt 
                  # seem feasible to redirect the keyboard to the container, the mouse is 
                   # is correctly redirected to the container, however, pyautogui display does not 
                    # like the keyboard at ALL, fixing this would be great, such that they can 
                     # take the pictures from within the container display, ignoring the screen on the 
                      # the outside machine, because the color or something I dont quite understand, 
                       # may be off in the outside machine, changing the picture somehow, which would 
                        # kind of break the thing
            with EasyProcess(running_command) as app_process: 
                if is_running_screenshot_tool_in_thread:
                    from screenshot_tool import \
                        screenshot_tool_parse_arguments, \
                        run_screenshot_tool_manually
                    template_match_image_to_test_photo_against_list, \
                        coords, \
                        recording_method, \
                        callback_type_str, \
                        app_to_test, \
                        actions_to_put_images_in, \
                        screenshot_file_name_list = \
                        screenshot_tool_parse_arguments(args)
                    # TODO find all screenshot_file_name_list automatically
                    screenshots_dir_per_action = find_screenshot_dirs_per_action(is_testing_in_cli, app_to_test, actions_to_put_images_in)
                    run_screenshot_tool_manually(
                        template_match_image_to_test_photo_against_list,
                        coords,
                        recording_method,
                        callback_type_str,
                        screenshots_dir_per_action,
                        screenshot_file_name_list,
                    )
                while True:
                    inp = input("q to shutdown container and quit\n")
                    if inp.strip().lower() == "q":
                        break
        except FileNotFoundError as e:
            print(e)
            print()
            print("java is probably not installed, try and install, running the script with --install_java y")
            print()
    
