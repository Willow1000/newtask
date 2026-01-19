import fire
import os 
import sys
 
sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
from testing.Test import Test


class ObjectMarkersTest(Test):
    def get_action_base_path(self):
        return os.path.dirname(__file__)
     
    def hooks_setup(self):
        hooks = {
            'shift_right_click': {
                "check": self.defaultHook,
            }, 
        }
        self.set_hooks(hooks)
     
    def main_test(self, action_ordered_steps_current_action):
        from object_markers.action_description import toggle_plugin
        from object_markers.action_description import cleanup_plugin
        from runescape_actions.commons.toggle_plugin.action_tests import TogglePluginTest
        from runescape_actions.commons.cleanup_plugin.action_tests import CleanupPluginTest
        from object_markers.action_description import mark_object

        self.incorporate_test(TogglePluginTest, toggle_plugin)
        self.incorporate_test(CleanupPluginTest, cleanup_plugin)
        self.test(mark_object)

    def run(self):
        print('testing object markers')
        # import everything you need from action_description here
        from object_markers.action_description import time_limit, current_action_id, \
            app_config_id, context 
        # from action_description import action_ordered_steps
        from object_markers.action_description import action_ordered_steps
        # you can have the full action test, or test step by step with singular functions
        self.full_test(None)
         
         
if __name__ == "__main__":
    # test
    print('make sure you run this utility from the directory outside of the runescape_actions directory')
    fire.Fire(ObjectMarkersTest)
