import os 
import sys
import cv2
import shutil

from PIL import Image


'''
requirements:
must be used by running whatever uses this from the directory that contains runescape_actions directory,
 this is because the sys.path.append below is relative to the directory that the script is run from
'''

# careful where you run this from, check requirements: at the start of this file
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
sys.path.append(os.path.join(os.getcwd(), 'LocallyAvailableActionTooling'))

from local_compare_to_test_field_script import compare_icon_to_image_list
from runelite_cv.testing import Testing
from runelite_cv.testing import draw_cross

global parent_action_name_g

color_code_dictionary = {
    "check": {"color_name": "red", "value": (0, 0, 255)},
    "verify": {"color_name": "green", "value": (0, 255, 0)},
    "jump": {"color_name": "yellow", "value": (255, 255, 0)},
    "others": {"color_name": "blue", "value": (255, 0, 0)},
}

manually_set_precision = 0.6  # default is 0.6

class NoComponentError(Exception):
    """Error raised when verification component is missing."""
    pass


def set_global_precision(precision: float):
    global manually_set_precision
    manually_set_precision = precision


def create_directory_if_not_exists(directory_path):
    """Creates a directory if it doesn't already exist.
    Args:
        directory_path (str): The path of the directory to create.
    """
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Directory created or already exists: {directory_path}")
    except Exception as e:
        print(f"An error occurred while creating the directory: {e}")


def report_on_current_test_element():
    '''
    report on the current test element
    '''
    # TODO: add information to output report
    return ''


def build_action_sreenshot_path(action_name): 
    '''
    return: path to the action screenshots from the directory outside this repo
    '''
    return f'runescape_actions/runescape_actions/{action_name}/all_action_files/screenshots/'


def build_icon_image(action_screenshot_path, icon_image):
    global parent_action_name_g
    if icon_image.startswith('all/'): 
        common_photos_path = "./runescape_actions/runescape_actions/commons/0common_photos/" 
        icon_image_in_main_path = f"{ common_photos_path }/{ icon_image[4:] }"
    else:
        icon_image_in_main_path = f'{action_screenshot_path}/{icon_image}'
        if not os.path.exists(icon_image_in_main_path): 
            icon_image_in_main_path = f'{ parent_action_name_g }/all_action_files/screenshots/{ icon_image }'
            return icon_image_in_main_path 
    return icon_image_in_main_path
      

def build_background_images_to_find(action_screenshot_path, background_images_to_find_icon_in_list):
    global parent_action_name_g
    # background_images_to_find_icon_in_list = [f'{action_screenshot_path}/{i}' for i in background_images_to_find_icon_in_list]
    new_background_images_to_find_icon_in_list = []
    unique_background_images = []
    for background_img in background_images_to_find_icon_in_list:
        if background_img.startswith('all/'): 
            common_photos_path = "./runescape_actions/runescape_actions/commons/0common_photos/" 
            background_img_full = f"{common_photos_path}/{background_img[4:]}"
        else:
            background_img_full = f'{action_screenshot_path}/{background_img}'
        if os.path.exists(background_img_full):
            new_background_images_to_find_icon_in_list.append(background_img_full)
        else:
            image_name = f'{ parent_action_name_g }/all_action_files/screenshots/{ background_img }' 
            new_background_images_to_find_icon_in_list.append(image_name)
            unique_background_images.append(image_name)
    return new_background_images_to_find_icon_in_list, unique_background_images
             
 
def parse_element_args_into_filename(filename, element_args):
    output_image_path_name = filename
    try:
        reverse_verify = element_args["reverse_verification"] 
        reverse_verify_exists = True
    except KeyError as e:
        reverse_verify_exists = False
    if reverse_verify_exists:
        output_image_path_name = f'{filename}_reverse_verify_should_be_black_img' 
    return output_image_path_name
 
 
def test_image_against_test_image(element_args, icon_image, background_images_to_find_icon_in_list, 
                                  step_num, iteration, action_name, test_element_type, 
                                  output_path=None): 
    '''
    background_images_to_find_icon_in_list: this is actually a single element, however, it's a single 
     element inside a list
    tests 'check' and 'verify' components of an image, against their test images
    iteration: this is the number of the test you are testing, in the action_description, a test list 
     is provided, this is the number of the test in that list
    return: report string
    '''
    global parent_action_name_g
    global manually_set_precision
     
    action_screenshot_path = build_action_sreenshot_path(action_name)
    background_images_to_find_icon_in_list, unique_background_images = \
        build_background_images_to_find(action_screenshot_path, background_images_to_find_icon_in_list)
    icon_image = build_icon_image(action_screenshot_path, icon_image)
    report, match_result = compare_icon_to_image_list(
        icon_image, background_images_to_find_icon_in_list, 
        algorithm='template_match',
        precision=manually_set_precision 
    )
    # match_result is a tuple with: (match_result_x, match_result_y, precision) 
    action_name_dir = action_name.split('/')[-1].split('.')[0]
    image_name = icon_image.split('/')[-1].split('.')[0] # get last element of image path and remove extension

    output_image_path_name = f'{step_num}_{image_name}_iteration_{iteration}_{ test_element_type }' 
    output_image_path_name = parse_element_args_into_filename(output_image_path_name, element_args)
    output_image_path_name = f'{output_image_path_name}.png'

    original_output_path = output_path
    save_full_report_path = f'local_test_output/{action_name_dir}/'
    if output_path is None:
        output_image_dir = save_full_report_path
        output_image_path = f'{output_image_dir}/{output_image_path_name}'
    else:
        output_image_dir = output_path
        output_image_path = f'{output_image_dir}/{output_image_path_name}'
    # create a dir that doesnt exist
    create_directory_if_not_exists(output_image_dir)
    first_output_dir = f'{ output_image_dir }/{ output_image_path_name }'
    if original_output_path is not None: 
        output_image_path = f'{output_image_dir}/{output_image_path_name}'
        # TODO why was this here?
        # output_image_path = ''.join(output_image_path.replace('//', '/').split(output_image_path_name))
        # output_image_path = '/'.join( output_image_path.split('/')[:-3] )
        # output_image_path = f'{output_image_path}/{ output_image_path_name }' 
    report += f'test element: {icon_image}\n'
    report += f'output image path: {output_image_path}\n'

    match_coords = match_result[:2]
    precision = match_result[2]
    # I want to set a red cross in the test image where the icon is found, the icon position is the match_coords
     
    if not test_element_type in color_code_dictionary:
        msg = f"test_element_type: {test_element_type} not found in color_code_dictionary" 
        print(msg)
        report += msg
        test_element_type = "others"
    color = color_code_dictionary[test_element_type]["value"]

    for background_image in background_images_to_find_icon_in_list:
        if precision > manually_set_precision: 
            report += draw_cross(background_image, output_image_path, match_coords, color=color)
            report += draw_cross(background_image, first_output_dir, match_coords, color=color)
        else:
            report += f'precision is too low, black image created: {precision}\n'
            black_image = Image.new('RGB', Image.open(background_image).size, color='black')
            black_image.save(first_output_dir)
            black_image.save(output_image_path)
         
        if background_image in unique_background_images:
            # this is to create an unique image for the unique_images_for_this_test folder of the parent action
            parent_action = os.path.basename(parent_action_name_g.rstrip(os.sep))
            out_path = f'local_test_output/{parent_action}/unique_images_for_this_test/'
            new_out_path = f'{out_path}/{output_image_path.split("/")[-1]}'
            if precision > manually_set_precision:
                report += draw_cross(background_image, new_out_path, match_coords, color=color)
            else:
                # I want to know if the image was not found
                black_image = Image.new('RGB', Image.open(background_image).size, color='black')
                black_image.save(new_out_path)
    return report, unique_background_images


def callable_element_handle(element, element_args, test_element, hook_callable_func, step_num): 
    if hook_callable_func is not None:
        element_args.update({ 'step_num': step_num })
        out = hook_callable_func(element, element_args, test_element)
        return out
    else:
        # you probably want a do nothing hook instead of running the element, running it will 
         # probably never work
        element(element_args)
        return ''


def handle_test_element(element, element_args, test_element, test_element_list, step_num, action_name,
                        hook_callable_func, full_report, test_element_type, 
                        current_iteration=0, 
                        output_path=None): 
    '''
    test_element: will be None if there isnt one in the action description, this is allowed, mainly 
     because I want to run the callable elements even if the test is non-existant
    '''
    unique_background_images = []
    if callable(element):
        out = callable_element_handle(
            element, element_args, test_element, hook_callable_func, step_num
        )
        if isinstance(out, str):
            full_report += out
        elif isinstance(out, dict):
            full_report += out.get('report', '')
            element = out["element"]  # output element for testing, if there is a need for this
    if isinstance(element, str):
        # tests how precise an image is in its test image
        icon_image = element
        if test_element is not None and not isinstance(test_element, list):
            background_images_to_find_icon_in_list = [ test_element ]
            full_report_str_out, unique_background_images = test_image_against_test_image(
                element_args,
                icon_image,
                background_images_to_find_icon_in_list,
                step_num,
                current_iteration,
                action_name,
                test_element_type,
                output_path,
            )
            full_report += full_report_str_out
        else:
            # I allowed for test_element to be None, cause I also want to be able to run callable elements if 
             # the test is none
            full_report += 'no test element provided'
    elif isinstance(element, list):
        for single_ele in element:
            full_rep, background_imgs_u = handle_test_element(
                single_ele,
                element_args,
                test_element,
                test_element_list,
                step_num,
                action_name,
                hook_callable_func,
                full_report,
                test_element_type,
                current_iteration=current_iteration,
                output_path=output_path, 
            )
            full_report += full_rep
            unique_background_images += background_imgs_u
    full_report += report_on_current_test_element()
    return full_report, unique_background_images.copy()

 
def test_element(element, element_args, test_element_list, step_num, action_name, element_type,
                 hook_callable_func=None,
                 output_path=None) -> str: 
    full_report = ''
    current_iteration = 0
    if test_element_list:
        for test_element in test_element_list:
            full_report, unique_background_images = handle_test_element(element, element_args, test_element, test_element_list,  
                                step_num, action_name, hook_callable_func, full_report, element_type,
                                current_iteration, output_path) 
            current_iteration += 1
    else:
        full_report, unique_background_images = handle_test_element(element, element_args, test_element_list, test_element_list,  
                                          step_num, action_name, hook_callable_func, full_report, 
                                          element_type, current_iteration, output_path)
    return full_report, unique_background_images 
     
 
def handle_mock_image(mock_image) -> str | None:
    if mock_image is None:
        return None
    if callable(mock_image):
        # if mock_image is a callable, call it
        mock_image = mock_image()
    return mock_image
 
 
def test_jump(step, step_num, action_name, hook_callables_for_step, output_path=None):   
    '''
    must test the jump component against the 'test' image AND against the 'extra_test_info' image
    '''
    step_id = step["id"]
    test_element_type = 'jump'
    report = f'\nreport for step:\nstep num:{step_num}\nstep id:{step_id}\nelement:{test_element_type}\n'
    report += 'testing jump component\n\n'

    if hook_callables_for_step is not None:
        try:
            hook = hook_callables_for_step["verify"]  # jump uses verify hook
        except KeyError:
            hook = None
    else:
        hook = None

    try:
        element = step["jump"]["verify"]
    except KeyError as e:
        raise NoComponentError("No jump component found or no verify inside jump component found")
    try:
        check_args = step["check_args"]
    except KeyError:
        check_args = {}

    background_images_paths = step.get("test", [])
    background_images_to_find_icon_in_list = []
    for image_path in background_images_paths:
        mock_image = handle_mock_image(image_path['mock_image'])
        background_images_to_find_icon_in_list.append(mock_image)

    out = step.get("extra_test_info", {}).get("loop_info", {}).get("img_after_loop", None)
    if out is None:
        print("no extra_test_info found, for current jump component, this means: no ending test image") 
    else:
        background_images_to_find_icon_in_list += [out]

    report_out, unique_background_images = test_report_for_step(
        step_num,
        element,
        check_args,
        background_images_to_find_icon_in_list,
        step,
        action_name,
        hook,
        step_id,
        test_element_type,
        output_path,
    )
    report += report_out
    return report, unique_background_images 
         
 
def test_check(step, step_num, action_name, hook_callables_for_step, output_path=None):  
    '''
    displays 'test' image one by one, and tests the 'check' component against the 'test' image
    '''
    step_id = step["id"]
    test_element_type = 'check'
    report = f'\nreport for step:\nstep num:{step_num}\nstep id:{step_id}\nelement:{test_element_type}\n'
    report += 'testing check component\n\n'
    if hook_callables_for_step is not None:
        try:
            hook = hook_callables_for_step["check"]
        except KeyError:
            hook = None
    else:
        hook = None
    try:
        element = step["check"]
    except KeyError as e:
        raise NoComponentError("No check component found.")
    try:
        check_args = step["check_args"]
    except KeyError:
        check_args = {}

    try:
        background_images_paths = step["test"]
    except KeyError:
        background_images_paths = []
    background_images_to_find_icon_in_list = []
    for image_path in background_images_paths:
        mock_image = handle_mock_image(image_path['mock_image'])
        background_images_to_find_icon_in_list.append(mock_image)

    report_out, unique_background_images = test_report_for_step(
        step_num,
        element,
        check_args,
        background_images_to_find_icon_in_list,
        step,
        action_name,
        hook,
        step_id,
        test_element_type,
        output_path,
    )
    report += report_out
    return report, unique_background_images 


def test_verify(step, step_num, action_name, next_step_dict, hook_callables_for_step=None, output_path=None): 
    '''
    displays 'extra_test_info' image one by one, and tests the 'verify' component against the image
    '''
    step_id = step["id"]
    test_element_type = 'verify'
    report = f'\nreport for step:\nstep num:{step_num}\nstep id:{step_id}\nelement:{test_element_type}\n'
    report += 'testing verify component\n\n'
    if hook_callables_for_step is not None:
        try:
            hook = hook_callables_for_step["verify"]
        except KeyError:
            hook = None
    else:
        hook = None
     
    try:
        element = step["verify"]
    except KeyError as e:
        raise NoComponentError("No verify component found.")
    try:
        verify_args = step["verify_args"]
    except KeyError:
        verify_args = {}
     
    try:
        background_images_paths = step["extra_test_info"]
        verify_test_element = background_images_paths['end_mock_image_list']
    except KeyError:
        verify_test_element = []

    if not verify_test_element and not next_step_dict is None:
        # if there is no manually set verify test element, just use the next step's test element by default
        next_element_test_list = next_step_dict.get("test", [])
        verify_test_element.extend([handle_mock_image(image_dict.get( 'mock_image', None )) for image_dict in next_element_test_list])
     
    step_id = step["id"]
    test_element_type = 'verify'
    report_out, unique_background_images = test_report_for_step(
        step_num,
        element,
        verify_args,
        verify_test_element,
        step,
        action_name,
        hook,
        step_id,
        test_element_type,
        output_path,
    )
    report += report_out
    return report, unique_background_images 
 

def test_report_for_step(step_num, element, element_args, background_images_to_find_icon_in_list,
                    step, action_name, hook, step_id, test_element_type, output_path=None):  
    report, unique_background_images = test_element(element, element_args, background_images_to_find_icon_in_list, 
                           step_num, action_name, test_element_type, hook, output_path) 
    report += f'\ntested component for step: {step_id}\nstep num: {str( step_num )},\nelement was of type: {test_element_type}\n' 
    return report, unique_background_images 


def test_step(step, step_num, action_name, next_step_dict, hook_callables_for_step=None, output_path=None): 
    unique_background_images = []
    report = ''
    try:
        report_out, unique_background_images_out = test_jump(step, step_num, action_name, hook_callables_for_step, output_path)
        report += report_out
        unique_background_images += unique_background_images_out.copy()
    except NoComponentError as e:
        print("no jump component found")
    try:
        report_out, unique_background_images_out = test_check(step, step_num, action_name, hook_callables_for_step, output_path)
        report += report_out
        unique_background_images += unique_background_images_out.copy()
    except NoComponentError as e:
        print("no check component found")
    try:
        report_out, unique_background_images_out = test_verify(step, step_num, action_name, next_step_dict,  hook_callables_for_step, output_path) 
        report += report_out
        unique_background_images += unique_background_images_out.copy()
    except NoComponentError as e:
        print("no verify component found")
    return report, unique_background_images

def filter_step_id(step_id):
    pass

def find_partial_id_by_full_step_id(step_id, all_partial_step_ids: list):
    # always returns something
    partial_id = None
    for partial_id in all_partial_step_ids:
        if partial_id in step_id:
            print(f'found partial id: {partial_id} for step_id: {step_id}')
            return partial_id
    assert partial_id is not None, f"no partial id found for step_id: {step_id}"

def test(action_ordered_steps, action_name, parent_action_name, hook_callable_func_dict=None, output_path=None, step_num=0):
    '''
    hook_callable_func_dict: dictionary of hook functions that will call the 
     'check' and 'verify' function fields
    '''
    global parent_action_name_g
    step_num = step_num
    full_report = 'end of debug logs\n\n\nstart of full report:\n\n'

    parent_action_name_g = parent_action_name 
    unique_background_images = []
    total_num_steps = len(action_ordered_steps)
    for step_num, step_dict in enumerate(action_ordered_steps):
        step_id = step_dict["id"]
        step_id = step_id.lower().strip()
        if hook_callable_func_dict is not None:
            try:
                # I want to see if hook_callable_func_dict contains the partial string step_id in its keys
                if any(key in step_id for key in hook_callable_func_dict.keys()):
                    partial_step_id = find_partial_id_by_full_step_id(step_id, hook_callable_func_dict.keys())
                    hook_callables_for_step = hook_callable_func_dict[partial_step_id]
                else: 
                    hook_callables_for_step = None
            except KeyError:
                hook_callables_for_step = None
                 
        else:
            hook_callables_for_step = None
        print(f'testing step: {step_id}, step num: {step_num}')
        next_step_dict = action_ordered_steps[step_num + 1] if step_num + 1 < total_num_steps else None
        report_out, unique_background_images_out = test_step(
            step_dict,
            step_num,
            action_name,
            next_step_dict,
            hook_callables_for_step=hook_callables_for_step,
            output_path=output_path,
        ) 
        unique_background_images += unique_background_images_out.copy()
        full_report += report_out
    print()
    print(full_report)
    return full_report, step_num, unique_background_images


def save_all_pngs_to_output_path(input_path, output_path, exception_list=[]):
    # recursively enters directory and saves all files ending in .png to output_path
    image_name_set = set()
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith('.png'):
                if file in image_name_set or file in exception_list:
                    continue
                src_path = os.path.join(root, file)
                image_name_set.add(file)
                shutil.copy(src_path, output_path)


def save_all_unique_pngs_to_output_path(input_path, target_comparison_path, output_path, exception_list=[]): 
    '''
    recursively enters dir and adds all unique pngs to output_path
    recurses through input path and compares against target_comparison_path
    all unique pngs are saved to output_path
    '''
    print(f"color codes are: {color_code_dictionary}")

    image_names_in_target : set[str] = set()
    image_name_set : set[str] = set()
    duplicate_image_name_set : set[str] = set()
    for file in os.listdir(target_comparison_path):
        if file.lower().endswith('.png'):
            image_names_in_target.add(file)

    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith('.png'):
                image_name_set.add(file)

    for image_in_all_image_set in image_name_set:
        if image_in_all_image_set in image_names_in_target:
            duplicate_image_name_set.add(image_in_all_image_set)

    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith('.png'):
                if file in exception_list:
                    continue
                if file not in duplicate_image_name_set:
                    src_path = os.path.join(root, file)
                    image_name_set.add(file)
                    shutil.copy(src_path, output_path)


