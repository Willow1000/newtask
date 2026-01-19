import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class CraftBraceletTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'click_furnace': { 
                "check": self.hook_highlight_step,
            }, 
        }
        self.set_hooks(hooks)


    def main_test(self, action_ordered_steps_current_action):

        from craft_bracelet.action_description import withdraw_gold_bar
        from runescape_actions.commons.withdraw_bank.action_tests import WithdrawBankTest

        from craft_bracelet.action_description import deposit_gold_bracelet
        from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest

        from craft_bracelet.action_description import craft_bracelet
        # you can have the full action test, or test step by step with singular functions
            
        self.incorporate_test(WithdrawBankTest, withdraw_gold_bar)
        self.test(craft_bracelet)
        self.incorporate_test(DepositBankTest, deposit_gold_bracelet)
     
    def run(self):
        print('testing crafting gold bracelet')
        # import everything you need from action_description here
        from smelting_silver_bar.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(CraftBraceletTest)
