import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class InGamePause(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
        }
        self.set_hooks(hooks)


    def main_test(self, action_ordered_steps_current_action):
        from in_game_pause.action_description import action_ordered_steps
            
        # from highalching_combat_bracelet_at_fountain_of_rune.action_description import use_high_alch
        # self.incorporate_test(UseSpellTest, use_high_alch)
        self.test(action_ordered_steps)
     
    def run(self):
        print('testing in_game_pause')
        from in_game_pause.action_description import time_limit, current_action_id, \
            app_config_id, context 
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(InGamePause)
