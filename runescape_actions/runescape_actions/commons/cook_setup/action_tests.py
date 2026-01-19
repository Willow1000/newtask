import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class CookSetupTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
        }
        self.set_hooks(hooks)

    def main_test(self, action_ordered_steps_current_action):
        from cook_setup.action_description import (highlight_clerk, highlight_banker)
        from runescape_actions.commons.highlight_npc.action_tests import HighlightNpcTest

        from cook_setup.action_description import buy_items
        from runescape_actions.commons.buy_from_grand_exchange.action_tests import BuyFromGrandExchangeTest

        from cook_setup.action_description import (deposit_coins, deposit_logs, deposit_fish)
        from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest

        from cook_setup.action_description import (withdraw_logs, withdraw_fish)
        from runescape_actions.commons.withdraw_bank.action_tests import WithdrawBankTest
        # you can have the full action test, or test step by step with singular functions
            
        self.incorporate_test(HighlightNpcTest, highlight_clerk)
        self.incorporate_test(BuyFromGrandExchangeTest, buy_items)
        self.incorporate_test(HighlightNpcTest, highlight_banker)
        self.incorporate_test(DepositBankTest, deposit_coins)
        self.incorporate_test(DepositBankTest, deposit_logs)
        self.incorporate_test(DepositBankTest, deposit_fish)
        self.incorporate_test(WithdrawBankTest, withdraw_logs)
        self.incorporate_test(WithdrawBankTest, withdraw_fish)

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
    fire.Fire(CookSetupTest)
