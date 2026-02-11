import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class DepositBankTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__) 
     
    def hooks_setup(self):
        hooks = {
            'type_ammount': {
                "check": self.defaultHook,
            },
        }
        self.set_hooks(hooks)

    def main_test(self, action_ordered_steps_current_action):
        from deposit_bank.action_description import get_deposit_all_test, enter_bank, leave_bank
        from runescape_actions.commons.enter_bank.action_tests import EnterBankTest
        # from withdraw_bank.action_description import withdraw__bank
        from runescape_actions.commons.leave_bank.action_tests import LeaveBankTest

        self.incorporate_test(EnterBankTest, enter_bank)
        action_ordered_steps = get_deposit_all_test()
        self.test(action_ordered_steps)
        self.incorporate_test(LeaveBankTest, leave_bank)
     
    def run(self):
        print('testing deposit bank')
        # import everything you need from action_description here
        from deposit_bank.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(DepositBankTest)
