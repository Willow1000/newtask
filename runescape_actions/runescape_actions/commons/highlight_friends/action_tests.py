import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class HighlightFriendsTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'press_highlight_friends': { 
                "check": self.hook_template_matching,
            }, 
            'press_enable': { 
                "check": self.hook_template_matching,
            }, 
        }
        self.set_hooks(hooks)
    

    def run(self):
        print('testing highlight friends')
        # import everything you need from action_description here
        from highlight_friends.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        from highlight_friends.action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(action_ordered_steps)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(HighlightFriendsTest)
