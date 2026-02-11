import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test







class HighAlching(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            
        }
        self.set_hooks(hooks)

    def main_test(self, action_ordered_steps_current_action):
        from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest
        from runescape_actions.commons.withdraw_bank.action_tests import WithdrawBankTest
        from runescape_actions.commons.use_spell.action_tests import UseSpellTest

        from action_description import highalch_item,withdraw_nature_rune,withdraw_fire_staff, withdraw_item, custom_actions

        from runescape_actions.highalch_wrap_up.action_description import deposit_all_nature_rune,deposit_all_fire_staff
        # from highalch.action_description import (move_to_fountain_of_rune, move_to_underwall_tunnel)
        # from runescape_actions.commons.move_to.action_tests import MoveToTest

        # from highalch.action_description import use_high_alch
        # from runescape_actions.commons.use_spell.action_tests import UseSpellTest

        # from highalch.action_description import highalching_nature_rune
            
        self.incorporate_test(WithdrawBankTest,withdraw_nature_rune)
        self.incorporate_test(WithdrawBankTest, withdraw_fire_staff)
        self.incorporate_test(WithdrawBankTest, withdraw_item)
        self.incorporate_test(UseSpellTest,highalch_item)
        self.test(custom_actions)
        self.incorporate_test(DepositBankTest,deposit_all_nature_rune)
        self.incorporate_test(DepositBankTest,deposit_all_fire_staff)
     
    def run(self):
        print('testing HighAlching')
        # import everything you need from action_description here
        from highalch.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from highalch.action_description import action_ordered_steps    
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(HighAlching)
