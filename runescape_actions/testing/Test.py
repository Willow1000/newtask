import os
import sys
import shutil
import math

from PIL import ImageGrab
from PIL import Image

from abc import ABC, abstractmethod
from matplotlib.pyplot import step

from runelite_cv.testing import draw_cross
from .testing_lib import save_all_pngs_to_output_path
from .testing_lib import save_all_unique_pngs_to_output_path
from .testing_lib import set_global_precision


"""
Docs:
    to test the verify field, example:
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("test_existing_user"),
                get_test_picture_by_name("rs_app_requires_update"),
            ],
        },
    if you dont set this field, the default way to test the 'verify' field is it automatically checks the 'test' field of the next step 
     this means you can add a 'test' field to the final step in order to constantly test the 'verify' field
    to test the 'check' field, you can just add a 'test' field
    to test a 'jump' field, you can add a 'test' and an 'extra_test_info' field, to make sure something doesnt exist
"""


class Test(ABC):
    def __init__(
        self,
        current_action_list_projects_path,
        test_output_path=None,
        actions_project_path="",
        testing_lib_path="",
        parent_action_base_path=None,
        minimum_image_precision="0.6",
    ):
        set_global_precision(float( minimum_image_precision ))
        self.current_action_list_projects_path = current_action_list_projects_path
        self.actions_project_path = actions_project_path
        self.testing_lib_path = testing_lib_path
        self.parent_action_base_path = parent_action_base_path
        self.num_incorporated_test = 0 
        self.highlights_ran_num = 0

        self.other_test_class_type_dict: dict[type, int] = dict()
        self.unique_background_images: list[str] = list()

        # this step_id_ran_cnt just counts how many times a step has been ran 
        self.highlight_steps_ran_num = 0
        self.step_id_ran_cnt = {
            'default': 0,
        }

        action_base_path = self.get_action_base_path()
        action_base_path = self.generate_actions_base_path(action_base_path)
        self.action_base_path = action_base_path
        if test_output_path is None:
            test_output_path = 'local_test_output'
            output_path_name = os.path.basename(action_base_path)
            self.output_path = f'{ test_output_path }/{output_path_name}'
            if os.path.exists(self.output_path) and os.path.isdir(self.output_path):
                # Ensure that output_path is under 'local_test_output'
                local_test_output_abs = os.path.abspath('local_test_output')
                output_path_abs = os.path.abspath(self.output_path)
                if os.path.commonpath([output_path_abs, local_test_output_abs]) == local_test_output_abs:
                    shutil.rmtree(self.output_path)
                else:
                    raise Exception(f"Refusing to delete {self.output_path} as it is not under 'local_test_output'")
            os.makedirs(self.output_path, exist_ok=True)
        else:
            print(f'output path is:{ test_output_path }, since this is a custom path, not deleting path')
            self.output_path = test_output_path
        os.environ["CURRENT_ACTION_LIST_PROJECT_PATH"] = current_action_list_projects_path
        os.environ["ACTIONS_PROJECT_PATH"] = actions_project_path
        os.environ["TESTING_LIB_PATH"] = self.testing_lib_path 
        base = os.path.join(os.getcwd(), 'runescape_actions')
        sys.path.append(os.path.join(base, current_action_list_projects_path))
        sys.path.append(os.path.join(base, actions_project_path))
        sys.path.append(os.path.join(base, './'))
        # commons: common action directory
        sys.path.append(os.path.join(base, 'runescape_actions/commons'))
        sys.path.append(os.path.join(base, 'runescape_actions'))

        # action base path is the path of the action inside the actions directory
        self._hooks = {}
        self.final_output_string_with_all_warnings = ''
        self.full_report = ''
        self.step_num = 0

    def get_output_path(self):
        return self.output_path

    def generate_actions_base_path(self, action_base_path): 
        list_paths = os.path.normpath(action_base_path).split(os.sep)[-2:]
        if list_paths[-2] == 'commons':
            ret_path = '/'.join(list_paths)
        else:
            ret_path = list_paths[-1]
        return ret_path

    def set_hooks(self, hooks):
        self._hooks = hooks

    def get_hooks(self):
        return self._hooks

    @abstractmethod
    def hooks_setup(self):
        """
        notice you can prepended the action id and appended the step number, 
         appending the step number is not necssary, but its a good practice, 
          prepending the action id is not necessary, however, if not doing this, the override will happen 
           for every single step with the same step id, not just the step in this action
        there is a good example on how to do this in rs_login action tests
        """
        pass

    def basic_mock_test(self, function_received, args_to_func_received, test_element):
        '''
        this is your basic mock fctn, you can just use this whenever you want something that just 
         runs the functions and prints the output
        '''
        self.basic_hook_change_args_run_step(function_received, args_to_func_received, test_element)

    def basic_hook_change_args_run_step(self, function_received, args_to_func_received, test_element):
        args_to_func_received = self.mock_args(args_to_func_received) 
        output = function_received(args_to_func_received)
        print(f'output: {output}')

    def mock_args(self, args):
        '''
        override this method to set your own default mock args
        '''
        args = self.basic_mock_arguments(args)
        print('args')
        print(args)
        return args

    def basic_mock_arguments(self, args):
        args["args_by_func"] = args 
        args["reference_of_client_of_class"] = 'mock'
        args["input_from_previous_elements"] = 'mock'
        return args

    def mock_highlight_args(self, args_to_func_received, test_element="default") -> dict: 
        ''' 
        test_element: any basename you will be using, this will be incremented
        mock return for the highlight color step
        format is: BGR, and NOT RGB
        to use this function correctly for all the highlights in your actions, make sure to oveeride this, 
         this should return a list of dictionaries, each dictionary should have all the arguments for 
          your highlight function, mainly the color
        make sure to change "default" to the step id of the highlight you are trying to mock
        '''

        args = {}
        mock_d = self.add_highlight_color_args(args_to_func_received)
        test_element = f"{test_element}_{self.highlight_steps_ran_num}"
        args[test_element] = mock_d

        # self.step_id_ran_cnt[test_element] += 1
        return args

    def highlight_handler_by_step_id(self, args, dic):
        args['default'] = dic
        self.step_id_ran_cnt['default'] += 1
        return args

    def add_highlight_color_args(self, args_to_func_received, override_color_list:list=None):
        """
        :return: dictionary with color key, ready to be add to mock args
        """
        # default_color = (255, 255, 0)
        new_color_list = []
        if override_color_list is not None:
            if override_color_list is not list:
                raise ValueError("override_color must be a list")
            new_color_list = override_color_list 
        else:
            try: 
                new_color_list = args_to_func_received['args_by_func']['highlight_color']
                if not isinstance(new_color_list, list):
                    new_color_list = [ new_color_list ]
            except KeyError as e:
                # new_color_list = [ default_color ]
                print("no highlight color found, using default")
                raise e
        mock_d = {'highlight_color': new_color_list}
        return mock_d

    def handle_print_function_info(self, function_received, args_to_func_received, test_element):
        function_name = function_received.__name__ 
        output_str = f'function {function_name}\nwith arguments: {args_to_func_received}\nfor test element: {test_element}\n' 
        return output_str
     
    def hook_highlight_step(self, function_received, args_to_func_received, test_element):
        """
        what I want here is: to show the background (test image with the highlight) and then run the 
         press within highlight function, and see where it is pressed
        required arguments: 
            args_to_func_received: same has 
        """
        step_num = args_to_func_received['step_num']
        print( self.handle_print_function_info(function_received, args_to_func_received, test_element) )
        from .testing_lib import Testing
        testing: Testing
        testing = Testing()
        input_image_path = f'{self.current_action_list_projects_path}/{self.current_action_list_projects_path}/{ self.action_base_path }/all_action_files/screenshots/{ test_element }'
        output_path = f'{ self.output_path }/highlights/'
        os.makedirs(output_path, exist_ok=True)
         
        self.highlight_steps_ran_num = self.highlight_steps_ran_num + 1
        mock_arg_dict_by_test_element:dict = self.mock_highlight_args(args_to_func_received)
        test_element = f"{test_element}_{self.highlight_steps_ran_num}"
        mock_ret = mock_arg_dict_by_test_element.get(test_element, mock_arg_dict_by_test_element[f"default_{self.highlight_steps_ran_num}"])
        color_list = mock_ret['highlight_color']
         
        output_str = f'log for highlights step:\ninput_image_path: {input_image_path}\n' 
        output_str += f'output_path: {output_path}\n'
        output_str += f'testing element is: {test_element}\n'
        output_str += f'color_list: {color_list}\n'
        print(output_str)

        test_file_name = test_element.split('/')[-1].split('.')[0]
        test_file_name = f'{step_num}_{test_file_name}'
        output_str += testing.highlight(input_image_path, output_path, color_list, add_debug_info=False, full_output_image=test_file_name)
        return output_str

    def hook_template_matching(self, function_received, args_to_func_received, test_element):
        print( self.handle_print_function_info(function_received, args_to_func_received, test_element) )
        step_num = args_to_func_received['step_num']
        args_to_func_received = self.basic_mock_arguments(args_to_func_received)
        fn_args = args_to_func_received["args_by_func"]
        current_func_args = fn_args["template_match_for_step"]

        image_to_find = current_func_args["image_to_find"]
        precision = current_func_args["precision"]
        offset = current_func_args["offset"]
        test_element_full = os.path.join(self.current_action_list_projects_path, self.current_action_list_projects_path, self.action_base_path, 'all_action_files', 'screenshots', test_element)
        image_to_find_full = os.path.join(self.current_action_list_projects_path, self.current_action_list_projects_path, self.action_base_path, 'all_action_files', 'screenshots', image_to_find)
        image = Image.open( test_element_full )
        new_args = {
            "template_match_for_step": {
                "image_to_find": image_to_find_full,
                "image": image,
                "precision": precision,
                "offset": offset,
            },
        }
        new_args = self.basic_mock_arguments(new_args.copy())
        ret_dict = function_received(new_args)

        test_name = test_element.split('/')[-1].split('.')[0]
        test_name = f'{step_num}_{test_name}'
        output_path = f'{ self.output_path }/{ test_name }.png'
        coords = ret_dict[ "coords" ]
        precision = ret_dict[ "precision" ]
        if precision > 0.7:
            draw_cross(test_element_full, output_path, coords, (255, 0, 0))
        else:
            error_str = f'precision too low: {precision} for test element: {test_element}\n'
            self.final_output_string_with_all_warnings += error_str + '\n'
            print(error_str)
     
    def ignore_function(self, function_received, args_to_func_received, test_element):
        """
        function received is just the original function
        args_to_func_received is just the args to the original func, "verify_args"/"check_args" elements
        """
        output_str = self.handle_print_function_info(function_received, args_to_func_received, test_element)
        self.final_output_string_with_all_warnings += output_str + '\n'
        print(output_str)

    def replace_element_with_string(self, string_to_replace_with):
        """
        a lot of times I just wanted to replace the 'check'/'verify' elements with strings
        this is meant to be called inside another function
        """
        report = "replaced element currently being tested with string"
        print(report)
        element = string_to_replace_with
        out_d = {
            "report": report,
            "element": element,
        }
        return out_d
     
    def none_step_verify_hook(self, function_received, args_to_func_received, test_element):
        self.ignore_function(function_received, args_to_func_received, test_element)

    def test(self, action_ordered_steps):
        from .testing_lib import test
        # basic test
        self.hooks_setup()
        full_report, step_num, unique_background_images = test( 
            action_ordered_steps,
            self.action_base_path,
            self.parent_action_base_path,
            hook_callable_func_dict=self.get_hooks(),
            output_path=self.output_path,
            step_num=self.step_num,
        ) 
        self.unique_background_images += unique_background_images
        self.full_report += full_report + '\n'
        self.step_num = step_num
        return full_report

    def get_unique_background_images(self) -> list[str]:
        return self.unique_background_images

    def add_to_step_num(self, step_num):
        self.step_num += step_num

    def get_step_num(self):
        return self.step_num

    @abstractmethod
    def get_action_base_path(self):
        pass
     
    def incorporate_test(self, other_test_class : type, other_action_ordered_steps): 
        other_test : other_test_class
        class_name = other_test_class.__name__

        output_path_for_subclass = f'{self.output_path}/dependencies/{self.num_incorporated_test}_{class_name}/'
        self.num_incorporated_test += 1 
        os.makedirs(os.path.dirname(output_path_for_subclass), exist_ok=True)

        out_path = f'{self.output_path}/unique_images_for_this_test/'
        os.makedirs(out_path, exist_ok=True)

        other_test: Test = other_test_class(
            self.current_action_list_projects_path,
            test_output_path=output_path_for_subclass,
            parent_action_base_path=self.get_action_base_path(),
        )

        other_test.add_to_step_num(self.step_num)
        full_report = other_test.main_test(other_action_ordered_steps) 
        self.step_num += abs(self.step_num - other_test.get_step_num())
        exception_list = ['highlights']
        save_all_pngs_to_output_path(other_test.get_output_path(), self.output_path, exception_list) 

        unique_background_images_out = other_test.get_unique_background_images()
        self.unique_background_images += unique_background_images_out
        warnings, full_report = other_test.get_analysis()
        self.add_to_analysis(warnings, full_report)

    def main_test(self, action_ordered_steps):
        '''
        more complex tests will just overwrite this
        '''
        return self.test(action_ordered_steps)
     
    def full_test(self, action_ordered_steps): 
        '''
        you can just add all hooks to test in a dictionary or just create a function for each 
         step
        '''
        self.main_test(action_ordered_steps)
        self.output_analysis()

    def output_analysis(self):
        print('full report:')
        print(self.full_report)
        print()
        print('final output analysis, with warning and possible errors:')
        print(self.final_output_string_with_all_warnings)

        self.full_report += f'\n\nfinal output analysis, with warning and possible errors:\n{self.final_output_string_with_all_warnings}\n'

        action_name = self.action_base_path
        action_name_dir = action_name.split('/')[-1].split('.')[0] 
        save_full_report_path = f'local_test_output/{action_name_dir}/full_report_{action_name}.txt' 
        save_txt_to_file(save_full_report_path, self.full_report)
        print(f'saved report to file: {save_full_report_path}')

    def get_analysis(self):
        return self.final_output_string_with_all_warnings, self.full_report

    def add_to_analysis(self, analysis, full_report):
        self.final_output_string_with_all_warnings += f'{ analysis }\n'
        self.full_report += f'{ full_report }\n'

    def get_full_report(self):
        return self.full_report

    def defaultHook(self, function_received, args_to_func_received, test_element):
        print('ignoring this function:')
        self.ignore_function(function_received, args_to_func_received, test_element)

    @abstractmethod
    def run(self):
        pass


def save_txt_to_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file:
        file.write(content)


