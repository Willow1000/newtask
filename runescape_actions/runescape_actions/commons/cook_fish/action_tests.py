import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class CookFishTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'click_fire': { 
                "check": self.hook_highlight_step,
            }, 
        }
        self.set_hooks(hooks)

    def run(self):
        from cook_fish.action_description import cook_fish
        self.full_test(cook_fish)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(CookFishTest)
