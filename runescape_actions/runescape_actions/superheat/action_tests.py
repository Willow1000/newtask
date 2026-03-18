import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class SuperHeatingIronBarTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'check_if_already_on': { 
                "check": self.defaultHook,
            }, 
        }
        self.set_hooks(hooks)


    def main_test(self, action_ordered_steps_current_action):
        from superheating_iron_bar.action_description import (highlight_clerk, highlight_banker)
        from runescape_actions.commons.highlight_npc.action_tests import HighlightNpcTest


        from superheating_iron_bar.action_description import buy_items
        from runescape_actions.commons.buy_from_grand_exchange.action_tests import BuyFromGrandExchangeTest

        from superheating_iron_bar.action_description import (deposit_coins, deposit_iron_ore, deposit_iron_bar)
        from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest

        from superheating_iron_bar.action_description import withdraw_iron_ore
        from runescape_actions.commons.withdraw_bank.action_tests import WithdrawBankTest

        from superheating_iron_bar.action_description import use_superheat
        from runescape_actions.commons.use_spell.action_tests import UseSpellTest

        from superheating_iron_bar.action_description import superheating_iron_bar
        # you can have the full action test, or test step by step with singular functions
            
        self.incorporate_test(HighlightNpcTest, highlight_clerk)
        self.incorporate_test(BuyFromGrandExchangeTest, buy_items)
        self.incorporate_test(HighlightNpcTest, highlight_banker)

        self.incorporate_test(DepositBankTest, deposit_coins)
        self.incorporate_test(DepositBankTest, deposit_iron_ore)
        self.incorporate_test(WithdrawBankTest, withdraw_iron_ore)
        self.incorporate_test(UseSpellTest, use_superheat)
        self.incorporate_test(DepositBankTest, deposit_iron_bar)

        self.test(superheating_iron_bar)

    def run(self):
        print('testing superheating_iron_bar' )
        # import everything you need from action_description here
        from smelting_steel_bar_setup.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(SuperHeatingIronBarTest)
