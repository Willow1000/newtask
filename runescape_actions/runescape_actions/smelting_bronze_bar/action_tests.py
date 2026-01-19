import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class SmeltBronzeBarTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'move_to_edgeville': {
                "check": self.defaultHook,
            }, 
            'move_to_edgeville_furnace': {
                "check": self.defaultHook,
            }, 
            'move_to_edgeville_banker': {
                "check": self.defaultHook,
            }, 
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
        from smelting_bronze_bar.action_description import smelt_bronze_bar_setup
        from runescape_actions.smelting_bronze_bar_setup.action_tests import SmeltBronzeBarSetupTest

        from smelting_bronze_bar.action_description import highlight_banker
        from runescape_actions.commons.highlight_npc.action_tests import HighlightNpcTest

        from smelting_bronze_bar.action_description import withdraw_iron_ore
        from runescape_actions.commons.withdraw_bank.action_tests import WithdrawBankTest

        from smelting_bronze_bar.action_description import mark_furnace
        from runescape_actions.commons.object_markers.action_tests import ObjectMarkersTest

        from smelting_bronze_bar.action_description import smelt_bronze_bar
        from runescape_actions.commons.smelt_item.action_tests import SmeltItemTest

        from smelting_bronze_bar.action_description import deposit_bronze_bar
        from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest
            
        self.incorporate_test(SmeltBronzeBarSetupTest, smelt_bronze_bar_setup)
        self.incorporate_test(HighlightNpcTest, highlight_banker)
        self.incorporate_test(WithdrawBankTest, withdraw_iron_ore)
        self.incorporate_test(ObjectMarkersTest, mark_furnace)
        self.incorporate_test(SmeltItemTest, smelt_bronze_bar)
        self.incorporate_test(DepositBankTest, deposit_bronze_bar)
     
    def run(self):
        print('testing smelt bronze bar')
        # import everything you need from action_description here
        from smelting_bronze_bar.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(SmeltBronzeBarTest)
