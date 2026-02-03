# import fire
# import os 
# import sys
 
# sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
# from testing.Test import Test


# class HighAlchingNatureRune(Test):
#     def get_action_base_path(self):
#         return os.path.dirname(__file__)
     
#     def hooks_setup(self):
#         hooks = {
            
#         }
#         self.set_hooks(hooks)

#     # def main_test(self, action_ordered_steps_current_action):
#     #     # from highalch.action_description import (move_to_fountain_of_rune, move_to_underwall_tunnel)
#     #     # from runescape_actions.commons.move_to.action_tests import MoveToTest

#     #     # from highalch.action_description import use_high_alch
#     #     # from runescape_actions.commons.use_spell.action_tests import UseSpellTest

#     #     from highalch.action_description import highalching_nature_rune
            
#     #     # self.incorporate_test(MoveToTest, move_to_fountain_of_rune)
#     #     # self.incorporate_test(MoveToTest, move_to_underwall_tunnel)
#         self.incorporate_test(UseSpellTest, use_high_alch)
#     #     self.test(highalching_nature_rune)
     
#     def run(self):
#         print('testing HighAlchingNatureRune')
#         # import everything you need from action_description here
#         from highalch.action_description import time_limit, current_action_id, \
#             app_config_id, context 
#         from highalch.action_description import action_ordered_steps    
#         # from action_description import action_ordered_steps
#         # you can have the full action test, or test step by step with singular functions
#         self.full_test(action_ordered_steps)
         
         
# if __name__ == "__main__":
#     # test
#     print('make sure you run this utility from the directory outside of the runescape_actions directory')
#     fire.Fire(HighAlchingNatureRune)

import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class HighAlchingRuneLongsword(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            
        }
        self.set_hooks(hooks)


    def main_test(self, action_ordered_steps_current_action):
        # from highalching_combat_bracelet_at_fountain_of_rune.action_description import (move_to_fountain_of_rune, move_to_underwall_tunnel)
        # from runescape_actions.commons.move_to.action_tests import MoveToTest

        from highalching_combat_bracelet_at_fountain_of_rune.action_description import use_high_alch
        from runescape_actions.commons.use_spell.action_tests import UseSpellTest

        # from highalching_combat_bracelet_at_fountain_of_rune.action_description import highalching_combat_bracelet_at_fountain_of_rune
            
        # self.incorporate_test(MoveToTest, move_to_fountain_of_rune)
        # self.incorporate_test(MoveToTest, move_to_underwall_tunnel)
        self.incorporate_test(UseSpellTest, use_high_alch)
        # self.test(highalching_combat_bracelet_at_fountain_of_rune)
     
    def run(self):
        print('testing HighAlchingNatureRune')
        # import everything you need from action_description here
        from highalch.action_description import time_limit, current_action_id, \
            app_config_id, context 
        from highalch.action_description import action_ordered_steps    
        # from action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(action_ordered_steps)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(HighAlchingRuneLongsword)

