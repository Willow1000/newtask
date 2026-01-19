import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class SmeltIronBarTest(Test):
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
        from smelting_iron_bar.action_description import (highlight_clerk, highlight_banker, highlight_murky)
        from runescape_actions.commons.highlight_npc.action_tests import HighlightNpcTest
        from smelting_iron_bar.action_description import buy_items
        from runescape_actions.commons.buy_from_grand_exchange.action_tests import BuyFromGrandExchangeTest
        from smelting_iron_bar.action_description import buy_ring_from_murky_matt
        from runescape_actions.commons.buy_ring_from_murky_matt.action_tests import BuyRingFromMurkyMattTest
        from smelting_iron_bar.action_description import (deposit_coins, deposit_iron_ore, deposit_iron_bar)
        from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest

        from smelting_iron_bar.action_description import withdraw_iron_ore
        from runescape_actions.commons.withdraw_bank.action_tests import WithdrawBankTest
        from smelting_iron_bar.action_description import mark_furnace
        from runescape_actions.commons.object_markers.action_tests import ObjectMarkersTest
        from smelting_iron_bar.action_description import smelt_iron_bar
        from runescape_actions.commons.smelt_item.action_tests import SmeltItemTest

        # you can have the full action test, or test step by step with singular functions
        self.incorporate_test(HighlightNpcTest, highlight_clerk)
        self.incorporate_test(BuyFromGrandExchangeTest, buy_items)
        self.incorporate_test(HighlightNpcTest, highlight_murky)
        self.incorporate_test(BuyRingFromMurkyMattTest, buy_ring_from_murky_matt)
        self.incorporate_test(HighlightNpcTest, highlight_banker)
        self.incorporate_test(DepositBankTest, deposit_coins)
        self.incorporate_test(DepositBankTest, deposit_iron_ore)
        
        self.incorporate_test(HighlightNpcTest, highlight_banker)
        self.incorporate_test(WithdrawBankTest, withdraw_iron_ore)
        self.incorporate_test(ObjectMarkersTest, mark_furnace)
        self.incorporate_test(SmeltItemTest, smelt_iron_bar)
        self.incorporate_test(DepositBankTest, deposit_iron_bar)
     
    def run(self):
        print('testing smelt bronze bar')
        # import everything you need from action_description here
        from smelting_iron_bar.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(SmeltIronBarTest)
