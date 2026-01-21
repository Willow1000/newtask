import os
import sys
import time
import argparse
import shutil
import subprocess 
 
 
from screenshot_tool_lib import screenshot_tool_get_args
from screenshot_tool_lib import normalize_path
from screenshot_tool_lib import recursive_copy_and_overwrite
from screenshot_tool_lib import stop_docker_container
from screenshot_tool_lib import docker_exec
from screenshot_tool_lib import docker_start_hidden
from screenshot_tool_lib import read_lines_from_file
from screenshot_tool_lib import write_lines_to_file
from screenshot_tool_lib import delete_any

"""
python 'path_of_repo_in_local_system'/start_app_from_within_container_and_share_screen_script.py  --config run_config -data rs_bot_app --app_path_inside_container /opt/code/LocallyAvailableActionTooling/runelite-client-1.10.36-SNAPSHOT-shaded.jar --ip_display_combo 192.168.56.1:0.0 --install_java n --run_screenshot_tool_in_thread y --app_to_test runescape_actions --actions_to_put_images_in rs_login --is_test_container y --callback_type_str keyboard --x_axis_size 1280 --y_axis_size 640 --container_id local_container_tools
"""


def replace_lines_in_coords_file(input_file, output_file, coords_file_in, coords_file_out):
    changed_lines = []
    new_lines = []
    with open(coords_file_in, "r") as in_file, open(coords_file_out, "a") as out_file:
        lines_list = in_file.readlines()
        for line in lines_list:
            original_path = line.split(" : ")[0]
            normalized_path = normalize_path(original_path)
            print()
            print("original_path")
            print(original_path)
            print("normalized_path")
            print(normalized_path)
            print()
            # normalized_input_path = normalize_path(input_file)
            if "/opt/data" in normalized_path:
                line = line.replace(original_path, output_file)
                line = line.replace("C:/Users/dboy/PycharmProjects/botcode", "/opt/code")
                changed_lines.append(line)
            new_lines.append(line)
        out_file.writelines(changed_lines)
    with open(coords_file_in, "w") as file:
        file.writelines(new_lines)


def recursively_copy_fotos(dir_to_output_images_to, new_photo_path, coords_file_in, coords_file_out):
    for foto_path in os.listdir(new_photo_path):
        next_photo_path_to_check = new_photo_path + "/" + foto_path
        new_dir_to_output_images_to = dir_to_output_images_to + "/" \
                                      + foto_path
        if "coord_logs" in next_photo_path_to_check:
            continue
        else:
            print("updating coord_logs file")
            replace_lines_in_coords_file(next_photo_path_to_check, new_dir_to_output_images_to, coords_file_in, coords_file_out)
            print()
            print("copying image from temp file: " + next_photo_path_to_check)
            print("copying image into: " + new_dir_to_output_images_to)
            print()
        if os.path.isfile(next_photo_path_to_check):
            src = next_photo_path_to_check
            dst = new_dir_to_output_images_to
            recursive_copy_and_overwrite(src, dst)
        else:
            new_next_photo_path_to_check = next_photo_path_to_check + "/"
            new_dir_to_output_images_to = new_dir_to_output_images_to + "/"
            recursively_copy_fotos(new_dir_to_output_images_to,
                                   new_next_photo_path_to_check,
                                   coords_file_in,
                                   coords_file_out)


def raw_screenshot_tool_parse_arguments(args):
    x_axis_size = "--x_axis_size " + args.x_axis_size
    y_axis_size = "--y_axis_size " + args.y_axis_size
    coords = "--coords " + args.coords
    recording_method = "--recording_method " + args.recording_method
    callback_type_str = "--callback_type_str " + args.callback_type_str
    app_to_test = "--app_to_test " + args.app_to_test
    actions_to_put_images_in = "--actions_to_put_images_in " + args.actions_to_put_images_in
    if args.screenshot_file_name_list is not None:
        screenshot_file_name_list = "--screenshot_file_name_list " + args.screenshot_file_name_list
    else:
        screenshot_file_name_list = ''
    if args.template_match_image_to_test_photo_against_list is not None:
        template_match_image_to_test_photo_against_list = "--template_match_image_to_test_photo_against_list " + args.template_match_image_to_test_photo_against_list.replace("\\", "/")
    else:
        template_match_image_to_test_photo_against_list = ""
    return template_match_image_to_test_photo_against_list, x_axis_size, y_axis_size, coords, recording_method, callback_type_str, app_to_test, actions_to_put_images_in, screenshot_file_name_list


def erase_duplicates_from_image_to_coords_association_file(dir_to_output_images_to):
    file_name = "coord_logs.txt"
    coords_logs_file_path = dir_to_output_images_to + "/" + file_name
    lines_list = read_lines_from_file(coords_logs_file_path)
    intermediate_dict = {}
    new_lines = []
    LINE_SEPARATOR = " : "
    for line in lines_list:
        split_line = line.split(LINE_SEPARATOR)
        line_path, coordsI, coordsF = split_line
        intermediate_dict[line_path] = coordsI + LINE_SEPARATOR + coordsF
    for line_path, coords in intermediate_dict.items():
        lew_line = line_path + LINE_SEPARATOR + coords
        new_lines.append(lew_line)
    write_lines_to_file(new_lines, coords_logs_file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--config",
                        help="used config name(ex: run_config)",
                        required=True)
    parser.add_argument("--container_id",
                        help="container id, default is centralized manager (however, some strange screen behavior may happen in other containers and further images may be required)",
                        required=True)
    parser.add_argument("-data", "--data_path_dir_name",
                        help="used dir name for current project's data (ex: rs_bot_app)",
                        required=True)
    parser.add_argument("--app_path_inside_container",
                        help="path to the LocallyAvailableActionTooling repo dir inside container",
                        required=True)
    parser.add_argument("--ip_display_combo",
                        help="ip and display number combo, ex: 'ip:display_number'",
                        required=True)
    parser.add_argument("--install_java",
                        help="[y/N] updates java version to path /opt/'java_version'",
                        default="n")
    parser.add_argument("--run_screenshot_tool_in_thread",
                        help="[y/N] run screenshot tool in thread, requires the other screenshot tool options",
                        default="n")
    parser.add_argument("--x_axis_size",
                        help="x axis size of screen",
                        default=1024)
    parser.add_argument("--y_axis_size",
                        help="y axis size of screen",
                        default=768)
    parser.add_argument("--username",
                        help="client container's username, required with container id",
                        default=None)
    parser.add_argument("--is_test_container",
                        help="[Y/n] created to know if you are running in a production client or \
                         a test container, where everything is already setup",
                        default='y')
    screenshot_tool_get_args(parser)
    args = parser.parse_args()
    
    if args.username is not None:
        username = args.username.strip().lower()

    if args.is_test_container == "y":
        is_running_in_test_container = True
    else:
        is_running_in_test_container = False

    container_id = args.container_id.strip().lower()
    
    run_screenshot_tool_in_thread = args.run_screenshot_tool_in_thread.strip().lower()
    is_running_screenshot_tool_in_thread = False
    if run_screenshot_tool_in_thread == "y":
        is_running_screenshot_tool_in_thread = True
    install_java = args.install_java.strip().lower()
    is_installing_java = False
    if install_java == "y":
        is_installing_java = True
    app_path_inside_container = args.app_path_inside_container.strip()
    app_path_inside_container = f'{app_path_inside_container}/app-shaded.jar'

    os.environ["CONFIG_NAME"] = args.config.strip().lower()
    print("config set to: " + os.environ["CONFIG_NAME"])
    os.environ["SERVER_SIDE_DATA_PATH"] = args.data_path_dir_name.strip().lower()
    
    if is_running_screenshot_tool_in_thread:
        # if is running screenshot tool, this will also accept the args of the screenshot tool
        add_running_screenshot_tool_thread = "--run_screenshot_tool_thread y "
    else:
        add_running_screenshot_tool_thread = "--run_screenshot_tool_thread n "
    raw_args = raw_screenshot_tool_parse_arguments(args)
    add_running_screenshot_tool_thread += ' '.join(raw_args)
    
    actions_to_put_images_in = raw_args[7]
    actions_to_put_images_in = actions_to_put_images_in.replace("--actions_to_put_images_in ", "")
    app_to_test = raw_args[6]
    app_to_test = app_to_test.replace("--app_to_test ", "")
    images_output = 'out_path' + "/" + app_to_test + "/" + app_to_test + "/" + actions_to_put_images_in + "/all_action_files/screenshots/"
    
    # this is a common ip-display combo, when running from inside the container
    ip_display_combo = args.ip_display_combo.strip().lower()
    print("ip_display_combo")
    print(ip_display_combo)
    
    print("starting container, wait for 5secs...")
    print("container_id the photoshoot is running in: " + container_id)
    
    docker_start_hidden(container_id)
    time.sleep(5)
    
    temp_container_id_list = [container_id]
    
    if is_installing_java:
        install_command = 'bash -lc \"cd /opt/; wget https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.6%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz; tar xfvz OpenJDK11U-jdk_x64_linux_hotspot_11.0.6_10.tar.gz\"'
        docker_exec(container_id, install_command)
        print("java packaged updated")
    
    # app should be in $OSRS_JAR_PATH/$OSRS_SHADED_JAR_VERSION
    java_bin_path = "/opt/jdk-11.0.6+10/bin/java"
    
    if is_running_in_test_container:
        start_app_command = java_bin_path + " -ea -cp net.runelite.client.RuneLite -jar " + app_path_inside_container + " --debug --developer-mode"
        arguments = add_running_screenshot_tool_thread + \
                    " --running_command \'" + start_app_command + "\'"
        script_path_inside_container = "/opt/code/LocallyAvailableActionTooling/inside_container_run_app_with_screenshot_tool.py"
        start_inside_container_run_app_with_screenshot_tool = \
            "/code/venv_inside_docker/bin/python " + script_path_inside_container + " " + arguments
        
        set_display_env_command = 'export DISPLAY=' + ip_display_combo
        
    else:
        # this else case is not working for now, needs to be fixed
        # TODO fix this
        # from configs.deployment.main_config import *
        # from environment.environment_setup.centralized_manager_environment_setup_config import *

        start_app_command = 'su ' + username + ' -c \\"' + java_bin_path + ' -ea -cp net.runelite.client.RuneLite -jar ' + app_path_inside_container + ' --debug --developer-mode\\"'
        arguments = add_running_screenshot_tool_thread + \
                    " --running_command \'" + start_app_command + "\'"
        script_path = "./inside_container_run_app_with_screenshot_tool.py"
        src = script_path
        container_types = os.listdir(all_containers_data_path)
        path_outside_container_to_copy_to = ""
        for i in container_types:
            path_to_test = all_containers_data_path + "/" + i
            container_ids_for_test = os.listdir(path_to_test)
            if container_id in container_ids_for_test:
                path_outside_container_to_copy_to = path_to_test + "/" + container_id + "/"
                break
        dst = new_script_path = path_outside_container_to_copy_to + "/" + script_path.split("/")[-1]
        copy_file(src, dst)
        
        management_scripts_path = "./management_scripts_utility"
        src = management_scripts_path
        management_script_utility_dir = path_outside_container_to_copy_to + "/" + management_scripts_path.split("/")[-1]
        dst = management_script_utility_dir
        recursive_copy_and_overwrite(src, dst)
        
        src = bot_framework_project_path
        dst = new_bot_framework_dir_inside_container = path_outside_container_to_copy_to + "/" + bot_framework_project_path.split("/")[-1]
        recursive_copy_and_overwrite(src, dst)
        
        new_photo_path = path_outside_container_to_copy_to + "/photos/"
        create_unexisting_dir(new_photo_path)
        create_unexisting_dir(new_photo_path + "action")
        create_unexisting_dir(new_photo_path + "action/worlds/")
        create_unexisting_dir(new_photo_path + "test")
        
        # copy coord_logs.txt
        src = coords_file_out = images_output +  "coord_logs.txt"
        dst = coords_file_in = new_photo_path + "/" + src.split("/")[-1]
        copy_file(src, dst)
        
        start_inside_container_run_app_with_screenshot_tool = \
            "/usr/bin/python3 " + "/opt/data/" + "inside_container_run_app_with_screenshot_tool.py " + arguments
        
        install_python_requirements_file_path = "/opt/data/management_scripts_utility/python_requirements.txt"
        cmd = "bash -lc \"" + install_python_requirements_file_path + "\""
        docker_exec(container_id, cmd)
        set_display_env_command = 'export DISPLAY=' + ip_display_combo + ";" \
                                  "export CLIENT_MANAGER_PROJECTS_PATH=/opt/data/" + ";" + \
                                  "export CLIENT_PROJECT_PATH=/opt/code/client_side/" + ";" + \
                                  "export TESTING_IN_CLIENT=1" + ";" + \
                                  "export BOT_FRAMEWORK_PATH=/opt/data/" + bot_framework_project_path.split("/")[-1] + "/"

    if os.name != 'nt':  # nt = Windows
        set_display_env_and_start_app_command = 'bash -lc \"' + start_inside_container_run_app_with_screenshot_tool + '\"'
    else:
        set_display_env_and_start_app_command = 'bash -lc \"' + set_display_env_command +\
        ';' + start_inside_container_run_app_with_screenshot_tool + '\"'

    print("set_display_env_and_start_app_command")
    print(set_display_env_and_start_app_command)
    docker_exec(container_id, set_display_env_and_start_app_command)
    # no longer stops the container
    # stop_docker_container(container_id)
    
    if not is_running_in_test_container:
        recursively_copy_fotos(images_output, new_photo_path,
                               coords_file_in, coords_file_out)
        erase_duplicates_from_image_to_coords_association_file(images_output)
        delete_any(new_script_path)
        delete_any(management_script_utility_dir)
        delete_any(new_bot_framework_dir_inside_container)
        delete_any(new_photo_path)
        print("successfully copied photos and deleted excess dirs")
    print("exiting...")


