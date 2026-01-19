import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class CookingRawAnchovies(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
        }
        self.set_hooks(hooks)


    def main_test(self, action_ordered_steps_current_action):

        from cooking_raw_anchovies.action_description import cook_raw_anchovies
        from runescape_actions.commons.cook_fish.action_tests import CookFishTest

        from cooking_raw_anchovies.action_description import deposit_cooked_anchovies
        from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest
            

        self.incorporate_test(CookFishTest, cook_raw_anchovies)
        self.incorporate_test(DepositBankTest, deposit_cooked_anchovies)
     
    def run(self):
        print('testing CookingRawAnchovies')
        # import everything you need from action_description here
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(CookingRawAnchovies)