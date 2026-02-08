import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class CraftRingSetupTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
        }
        self.set_hooks(hooks)

    def hook_type_amount(self, function_received, args_to_func_received):
        '''
        example of custom hook: 
         small example of adding functionality (adding logs with simple print statements)
          otherwise, this doesnt really need to be here, in hooks_setup you can see that 
           self.basic_mock_test will do the same as this function 
        '''
        print('hooking type_ammount id step') 
        print(args_to_func_received)
        self.basic_mock_test(function_received, args_to_func_received)

    def main_test(self, action_ordered_steps_current_action):
        from craft_ring_setup.action_description import (
            highlight_clerk,
            highlight_banker,
            buy_items,
            deposit_bars,
            deposit_coins,
            withdraw_ring_mold,
            withdraw_gold_bar,
        )
        from runescape_actions.commons.highlight_npc.action_tests import HighlightNpcTest
        from runescape_actions.commons.buy_from_grand_exchange.action_tests import BuyFromGrandExchangeTest
        from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest
        from runescape_actions.commons.withdraw_bank.action_tests import WithdrawBankTest
        # you can have the full action test, or test step by step with singular functions

        self.incorporate_test(HighlightNpcTest, highlight_clerk)
        self.incorporate_test(BuyFromGrandExchangeTest, buy_items)
        self.incorporate_test(HighlightNpcTest, highlight_banker)
        self.incorporate_test(DepositBankTest, deposit_bars)
        self.incorporate_test(DepositBankTest, deposit_coins)
        self.incorporate_test(WithdrawBankTest, withdraw_ring_mold)
        self.incorporate_test(WithdrawBankTest, withdraw_gold_bar)

    def run(self):
        print('testing craft ring setup')
        # import everything you need from action_description here
        from craft_ring_setup.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(CraftRingSetupTest)
