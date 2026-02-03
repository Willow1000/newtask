import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
)

class RSLoginTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)

    def get_test_world_string_test(self, function_received, args_to_func_received, test_element):
        new_element_str = get_action_picture_by_name("worlds/world_308")
        return self.replace_element_with_string(new_element_str)
     
    def get_test_world_verification_string(self, function_received, args_to_func_received, test_element):
        new_element_str = get_action_picture_by_name("worlds/world_308_verification")
        return self.replace_element_with_string(new_element_str)
     
    def hooks_setup(self):
        """
        in this example: notice I prepended the action id and the appended the step number, 
         appending the step number is not necssary, but its a good practice, 
          prepending the action id is not necessary, however, if not doing this, the override will happen 
           for every single step with the same step id, not just the step with this id in this action
        """
        hooks = {
            "rs_login_find_image_in_worlds": {
                "check": self.get_test_world_string_test, 
                "verify": self.none_step_verify_hook,
            }, 
            "random_movement_for_check_world_step": {
                "check": self.none_step_verify_hook,
            }, 
            "press_chosen_world_btn": {
                "check": self.get_test_world_string_test,
            }, 
            "loop_until_world_selected": {
                "verify": self.get_test_world_verification_string, 
            }, 
            "press_insert_username": {
                "verify": self.none_step_verify_hook,
            }, 
            "send_creds": {
                "check": self.none_step_verify_hook,
                "verify": self.none_step_verify_hook,
            }, 
            "await_by_verify_on_all_images_a_change_in_UI_is_verified_before_making_jump_decision": {
                "check": self.none_step_verify_hook,
            }, 
            "loop_until_login_successful": {
                "check": self.none_step_verify_hook,
            },
            "select_password_field_for_password_insertion": {
                "verify": self.none_step_verify_hook,
            },
            "delete_and_reinsert_pw": {
                "check": self.none_step_verify_hook,
                "verify": self.none_step_verify_hook,
            },
            "select_username_field_for_username_insertion": {
                "verify": self.none_step_verify_hook,
            },
            "delete_and_reinsert_username": {
                "check": self.none_step_verify_hook,
                "verify": self.none_step_verify_hook,
            },
            "loop_to_retry_login": {
                "verify": self.none_step_verify_hook,
            },
        }
        self.set_hooks(hooks)

    def run(self):
        print("testing rs login")
        # import everything you need from action_description here
        from rs_login.action_description import time_limit, current_action_id, \
            app_config_id, context 
        from rs_login.action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(action_ordered_steps)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(RSLoginTest)
