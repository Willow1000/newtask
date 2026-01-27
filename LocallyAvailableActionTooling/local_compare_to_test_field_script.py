import fire 
import os 
import importlib

from compare_specific_image_list_to_other_base_image import compare_icon_to_image_list

'''
purpose is to function as a local test, a 'pretest' before submitting to the discord server
 this should show if all the components of the action are being found in the base images,
this is always good to run because if you miss something in your action, the discord server test 
 will take a while and if it's a simple mistake it should be caught here and save you a bunch of time
this should be run outside the test action
'''


def parse_components_from_step(step):
    components = {}
    for component_id in step:
        try:
            components[component_id] = step[component_id]
        except KeyError as e:
            pass
    return components

     
def get_actions(package_with_actions_path, action_category, action_name_to_test):
    '''
    gets all actions not really the components
    '''
    dir_with_actions = package_with_actions_path + "/" + action_category
    list_dir = os.listdir(dir_with_actions)
    all_listed_actions = {}
    for action_name in list_dir:
        if ".git" in action_name or ".gitignore" in action_name or "commons" in action_name or "__init" in action_name or "__py" in action_name:
            continue
        if action_name != action_name_to_test:
            continue
        action_to_test_dir = dir_with_actions  + "/" + action_name
        action_description_to_import = action_to_test_dir + "/action_description.py"
        spec = importlib.util.spec_from_file_location("*", action_description_to_import)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        ordered_steps = foo.action_ordered_steps.copy()
        all_failure_elements = foo.all_failure_elements.copy()
        action_id = foo.current_action_id
        all_listed_actions[action_id] = {
            "steps": ordered_steps,
            "all_failure_elements": all_failure_elements,
            "action_name": action_name,
            "app_config_id": foo.app_config_id,
            "time_limit": foo.time_limit,
            "context": foo.context,
        }
    return all_listed_actions 


class LocalComp(object):
    def __init__(self, path_with_app_actions_repo, action_name, action_category, 
                 steps_to_skip_by_number):
        # fire auto turns separation by commas into a tuple
        self.steps_to_skip_by_number = steps_to_skip_by_number
        self.path_of_actions_repo = f'{ path_with_app_actions_repo }/{action_category}'
        self.action_dir_path = f'{ path_with_app_actions_repo }/{action_category}/'
        self.action_name = action_name
        self.action_category = action_category
        self.action_framework_dir = f'{ path_with_app_actions_repo }/{action_category}/common_action_framework/'
        path_with_screenshots_for_action = f'{ self.action_dir_path }/{action_category}/{action_name}/all_action_files/screenshots/'
        self.path_with_screenshots_for_action = path_with_screenshots_for_action 
        self.path_with_action_images = f'{ path_with_screenshots_for_action }/'
        self.path_with_test_images = f'{ path_with_screenshots_for_action }/'
        self.full_report_string = ''

    def run(self):
        '''
        run the local test
        '''
        print('running local test')
        os.environ["ACTIONS_PROJECT_PATH"] = f'{ self.path_of_actions_repo }/common_action_framework/'
        os.environ["CURRENT_ACTION_LIST_PROJECT_PATH"] = self.action_dir_path
        actions_list = get_actions(self.action_dir_path, self.action_category, self.action_name)
        step_num = 0
        is_skipping_steps = False
        if self.steps_to_skip_by_number is not None and isinstance(self.steps_to_skip_by_number, tuple):
            is_skipping_steps = True
        for action in actions_list:
            action_name = actions_list[action]['action_name']
            print(f'running local test on action: {action_name}')
            print(f'parsing components from step num: {step_num}')
            print(f'numbers of steps to skip: {self.steps_to_skip_by_number}')
            for step in actions_list[action]['steps']:
                if is_skipping_steps and step_num in self.steps_to_skip_by_number:
                    step_num += 1
                    continue
                if step_num in self.steps_to_skip_by_number:
                    step_num += 1
                    continue
                msg_to_report = f'running step number: {step_num}\n'
                self.full_report_string += msg_to_report
                components = parse_components_from_step(step)
                print(f'components: {components}')
                try:
                    check_comp = components['check']
                except KeyError as e:
                    check_comp = None
                try:
                    verify_comp = components['verify']
                except KeyError as e:
                    verify_comp = None
                test_image_list = []
                try:
                    for test_comp in components['test']:
                        try:
                            if isinstance(test_comp['mock_image'], list):
                                test_image_list += test_comp['mock_image']
                            elif isinstance(test_comp['mock_image'], str): 
                                test_image_list.append(test_comp['mock_image'])
                        except KeyError as e:
                            pass
                except KeyError as e:
                    test_comp = None
                try:
                    extra_test_info_comp = components['extra_test_info']
                    try:
                        end_mock_image_list = extra_test_info_comp['end_mock_image_list']
                    except KeyError as e:
                        end_mock_image_list = None
                except KeyError as e:
                    extra_test_info_comp = None

                self.component_test(check_comp, test_image_list)
                self.component_test(verify_comp, end_mock_image_list)

                step_num += 1 
        print()
        print()
        print(f'full report summary\n: {self.full_report_string}')

    def component_test(self, component_by_type, image_list_to_test_against):
        if isinstance( component_by_type, str ):
            msg_to_report = 'component against image list\n'
            print(msg_to_report)
            self.full_report_string += msg_to_report
            if image_list_to_test_against is not None:
                verify_comp = f'{ self.path_with_action_images }/{ component_by_type }'
                new_end_mock_image_list = []
                for i in image_list_to_test_against:
                    new_end_mock_image_list.append(f'{ self.path_with_test_images }/{ i }')
                report, match_result = compare_icon_to_image_list(verify_comp, new_end_mock_image_list) 
                self.full_report_string += report
            else:
                print('image list is None')
        else:
            print('component is not a string')

 
if __name__ == '__main__':
    fire.Fire(LocalComp)
     
     

