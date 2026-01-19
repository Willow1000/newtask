import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class WithdrawBankTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'type_ammount': { 
                "check": self.defaultHook,
            }, 
            'type_item_name': { 
                "check": self.defaultHook,
            }, 
            'right_click_item': {
                "check": self.defaultHook,
            }, 
        }
        self.set_hooks(hooks)
    
    def main_test(self, action_ordered_steps_current_action):
        from withdraw_bank.action_description import (enter_bank, leave_bank)
        from runescape_actions.commons.enter_bank.action_tests import EnterBankTest

        from withdraw_bank.action_description import withdraw__bank
        from runescape_actions.commons.leave_bank.action_tests import LeaveBankTest

        self.incorporate_test(EnterBankTest, enter_bank)
        self.test(withdraw__bank)
        self.incorporate_test(LeaveBankTest, leave_bank)
     
    def run(self):
        print('testing smelt bronze bar')
        # import everything you need from action_description here
        from withdraw_bank.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        from withdraw_bank.action_description import get_withdraw_x_test
        action_ordered_steps = get_withdraw_x_test()
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(WithdrawBankTest)
