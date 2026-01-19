import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test

class TeleportToGrandExchangeTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)

    def hooks_setup(self):
        hooks = {
             
        }
        self.set_hooks(hooks)

    def run(self):
        print("test teleport to grand exchange")
        # import everything you need from action_description here
        from teleport_to_exchange.action_description import time_limit, current_action_id, \
            app_config_id, context 
        from teleport_to_exchange.action_description import get_teleport_to_exchange_test
        # you can have the full action test, or test step by step with singular functions
        from runescape_actions.commons.teleport_action.action_tests import TeleportTest
        from runescape_actions.commons.teleport_action.action_description import action_ordered_steps as teleport

        self.incorporate_test(TeleportTest, teleport)
        self.test(get_teleport_to_exchange_test())
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(TeleportToGrandExchangeTest)
