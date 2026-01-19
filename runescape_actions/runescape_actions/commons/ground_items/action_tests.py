import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class GroundItemsTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'click_item_name_textbox': { 
                "check": self.hook_template_matching,
            }, 
            'type_npc_name': { 
                "check": self.hook_type_amount,
            }, 
        }
        self.set_hooks(hooks)

    def hook_type_amount(self, function_received, args_to_func_received, test_element):
        '''
        example of custom hook: 
         small example of adding functionality (adding logs with simple print statements)
          otherwise, this doesnt really need to be here, in hooks_setup you can see that 
           self.basic_mock_test will do the same as this function 
        '''
        print('hooking type_quantity and type_price id step') 
        print(args_to_func_received)
        #self.basic_mock_test(function_received, args_to_func_received, test_element)
    
    def run(self):
        print('testing toggle run')
        # import everything you need from action_description here
        from ground_items.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        from ground_items.action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(action_ordered_steps)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(GroundItemsTest)
