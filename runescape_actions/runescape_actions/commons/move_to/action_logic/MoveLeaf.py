import abc
import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_test_picture_by_name, 
    none_step_verify
    )
from common_action_framework.common_action_framework.common import left_click_highlighted 
from runescape_actions.commons.move_to.action_logic.Movement import Movement
 
class MoveLeaf(Movement, abc.ABC):
    def __init__(
        self,
        initialColor: tuple[str],
        finalColor: tuple[str],
        colorPatternSet: set[str],
        currentColorIndex: int,   # This is the current color index and must be initialized to -1
        movementId: str,
    ) -> None:
        super().__init__(initialColor, finalColor, colorPatternSet, currentColorIndex, movementId) 

    def get_final_color(self) -> tuple[str]:
        return super().getFinalColor()
    
    def get_current_color(self) -> str:
        colors = super().get_colors()
        index = super().getCurrentColorIndex()
        return colors[index]

    def get_next_color(self) -> str:
        colors = super().getColorPatternSet()
        if colors:
            new_index = (super().getCurrentColorIndex() + 1) % len(colors)
            return colors[new_index]        

    def get_previous_color(self) -> str:
        colors = super().getColorPatternSet()
        if colors:
            previous_index = (super().getCurrentColorIndex() - 1) % len(colors)
            return colors[previous_index]
        
    def increase_color_index(self):
        colors = super().getColorPatternSet()
        new_index = (super().getCurrentColorIndex() + 1) % len(colors)
        super().setCurrentColorIndex(new_index)


    def click_highlighted_local(self):
        return left_click_highlighted(self.get_next_color())
    
    def move(self) -> list:

        # Step 1: Click the next color 
        step_1 = {
            "check": self.click_highlighted_local, 
            "verify": left_click_highlighted(self.get_previous_color()),
            "verify_args": {
                "reverse_verification": True,
            }, 
            "test": [
                {
                    "mock_image": get_test_picture_by_name("to_red"),  
                    "replay_input": {"replay_type": "mouse", "coords": None},
                },
            ],
            "extra_test_info": {
                "end_mock_image_list": [
                get_test_picture_by_name("to_green")
                ],
            },
            "processor_info": {
                "processor_type": {
                    "check": "template_match",
                    "verify": "template_match",
                },
            },
            "id": "click_next_color",
        }

        # Step 2: increase the color index 

        step_2 = {
                    "check": self.increase_color_index,
                    "verify": none_step_verify,
                    "id": "increase_color_index",
                    "processor_info": {
                        "processor_type": {
                            "check": "template_match",
                            "verify": "template_match",
                        },
                    },
                }

        # Step 3: Jump Step to estabilish the loop

        step_3 = {
            "jump": {
                "step_num": "1",
                "verify": left_click_highlighted(self.get_final_color()),
                "verify_mode": "verify_once",
                "reverse_verification": False,
            },
            "test": [
                {
                    "mock_image": get_test_picture_by_name("test_initial"),
                    "replay_input": {
                        "replay_type": "NA",
                        "word_to_write": None,
                    },
                },
            ],
            "extra_test_info": {
                "loop_info": {
                    "num_iterations": 3,
                    "img_after_loop": get_test_picture_by_name("test_final_color"),
                },
            },
            "processor_info": {
                "processor_type": {
                    "check": "xdot_keyboard_processing",
                    "verify": "template_match",
                },
            },
            "id": "check_for_final_color",
        }

        final_step = {
            "check": none_step_verify,
            "verify": none_step_verify,
            "id": "mark_npc_final_step",
            "processor_info": {
                "processor_type": {
                    "check": "template_match",
                    "verify": "template_match",
                },
            },
        }

        action_ordered_steps = [step_1, step_2, step_3, final_step]
        # return copy.deepcopy(action_ordered_steps)
        return action_ordered_steps
    

    def moveTest(self) -> list:

            # Step 1: Click the next color 
            step_1 = {
                "check": "self.click_highlighted_local", 
                "verify": "left_click_highlighted(self.get_previous_color())",
                "verify_args": {
                    "reverse_verification": True,
                }, 
                "test": [
                    {
                        "mock_image": get_test_picture_by_name("to_red"),  
                        "replay_input": {"replay_type": "mouse", "coords": None},
                    },
                ],
                "extra_test_info": {
                    "end_mock_image_list": [
                    get_test_picture_by_name("to_green")
                    ],
                },
                "processor_info": {
                    "processor_type": {
                        "check": "template_match",
                        "verify": "template_match",
                    },
                },
                "id": "click_next_color",
            }

            # Step 2: increase the color index 

            step_2 = {
                        "check": self.increase_color_index,
                        "verify": none_step_verify,
                        "id": "increase_color_index",
                        "processor_info": {
                            "processor_type": {
                                "check": "template_match",
                                "verify": "template_match",
                            },
                        },
                    }

            # Step 3: Jump Step to estabilish the loop

            step_3 = {
                "jump": {
                    "step_num": "1",
                    "verify": "click_highlighted(self.get_final_color())",
                    "verify_mode": "verify_once",
                    "reverse_verification": False,
                },
                "test": [
                    {
                        "mock_image": get_test_picture_by_name("test_initial"),
                        "replay_input": {
                            "replay_type": "NA",
                            "word_to_write": None,
                        },
                    },
                ],
                "extra_test_info": {
                    "loop_info": {
                        "num_iterations": 3,
                        "img_after_loop": get_test_picture_by_name("test_final_color"),
                    },
                },
                "processor_info": {
                    "processor_type": {
                        "check": "xdot_keyboard_processing",
                        "verify": "template_match",
                    },
                },
                "id": "check_for_final_color",
            }

            final_step = {
                "check": none_step_verify,
                "verify": none_step_verify,
                "id": "mark_npc_final_step",
                "processor_info": {
                    "processor_type": {
                        "check": "template_match",
                        "verify": "template_match",
                    },
                },
            }

            action_ordered_steps = [step_1, step_2, step_3, final_step]
            # return copy.deepcopy(action_ordered_steps)
            return action_ordered_steps




