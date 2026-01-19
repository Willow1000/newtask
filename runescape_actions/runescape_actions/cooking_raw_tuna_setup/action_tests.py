import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class CookingRawTunaSetup(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
        }
        self.set_hooks(hooks)

    def main_test(self, action_ordered_steps_current_action):
        from cooking_raw_tuna_setup.action_description import action_ordered_steps
        from runescape_actions.commons.cook_setup.action_tests import CookSetupTest
        # you can have the full action test, or test step by step with singular functions
            
        self.incorporate_test(CookSetupTest, action_ordered_steps)

    def run(self):
        print('testing HighAlchingCombatBraceletSetup')
        # import everything you need from action_description here
        from highalching_combat_bracelet_at_fountain_of_rune_setup.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(CookingRawTunaSetup)
