import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class BuyFromGrandExchangeTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'ammount_to_buy': { 
                "check": self.hook_template_matching,
            }, 
            'set_price': { 
                "check": self.hook_template_matching,
            }, 
            'type_item_name': { 
                "check": self.defaultHook,
            },
            'type_quantity': { 
                "check": self.defaultHook,
            },
            'type_price': { 
                "check": self.defaultHook,
            },
        }
        self.set_hooks(hooks)
    
    def main_test(self, action_ordered_steps_current_action):
        from buy_from_grand_exchange.action_description import enter_exchange
        from runescape_actions.commons.enter_exchange.action_tests import EnterExchangeTest
        from buy_from_grand_exchange.action_description import get_buy_from_exchange_test
        from buy_from_grand_exchange.action_description import leave_exchange
        from runescape_actions.commons.leave_exchange.action_tests import LeaveExchangeTest
        # you can have the full action test, or test step by step with singular functions
         
        self.incorporate_test(EnterExchangeTest, enter_exchange)
        self.test(get_buy_from_exchange_test())
        self.incorporate_test(LeaveExchangeTest, leave_exchange)

    def run(self):
        print('testing buy from grand exchange')
        # import everything you need from action_description here
        from action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(BuyFromGrandExchangeTest)
