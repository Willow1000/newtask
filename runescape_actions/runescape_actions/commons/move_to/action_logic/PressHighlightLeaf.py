import copy
import abc
from common_action_framework.common_action_framework.basic_interaction import (
    get_test_picture_by_name, 
    none_step_verify
    )
from common_action_framework.common_action_framework.common import left_click_highlighted 
from runescape_actions.commons.move_to.action_logic.MoveLeaf import MoveLeaf

class PresHighlightLeaf(MoveLeaf, abc.ABC):
    def __init__(
        self,
        finalColor: tuple[str],
        movementId: str,
    ) -> None:
        super().__init__(initialColor=None, finalColor= finalColor, colorPatternSet=None, currentColorIndex=None, movementId= movementId)


    def move(self) -> None:

        # Step 1: Click the final color 
        step_1 = {
            "check": self.click_highlighted_local, 
            "verify": none_step_verify,
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

        action_ordered_steps = [step_1, final_step]
        return copy.deepcopy(action_ordered_steps)
