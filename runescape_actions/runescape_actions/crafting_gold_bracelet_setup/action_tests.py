import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class CraftGoldBraceletSetupTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
        }
        self.set_hooks(hooks)


    def main_test(self, action_ordered_steps_current_action):
        from crafting_gold_bracelet_setup.action_description import action_ordered_steps
        from runescape_actions.commons.craft_bracelet_setup.action_tests import CraftBraceletSetupTest
        # you can have the full action test, or test step by step with singular functions
            
        self.incorporate_test(CraftBraceletSetupTest, action_ordered_steps)

    def run(self):
        print('testing smelt bronze bar')
        # import everything you need from action_description here
        from smelting_silver_bar_setup.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(CraftGoldBraceletSetupTest)
