import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class MarkNpcTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'click_npc_to_mark': {
                "check": self.hook_right_click_item,
            }, 
            'click_marked_npc': {
                "check": self.hook_right_click_item,
            }, 
        }
        self.set_hooks(hooks)
    
    def hook_right_click_item(self, function_received, args_to_func_received):
        '''
        example of custom hook: 
         small example of adding functionality (adding logs with simple print statements)
          otherwise, this doesnt really need to be here, in hooks_setup you can see that 
           self.basic_mock_test will do the same as this function 
        '''
        print('hooking click_marked_npc and click_npc_to_mark id step') 
        print(args_to_func_received)
        #self.basic_mock_test(function_received, args_to_func_received)
     

    def run(self):
        print('testing toggle run')
        # import everything you need from action_description here
        from mark_npc.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        from mark_npc.action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(action_ordered_steps)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(MarkNpcTest)
