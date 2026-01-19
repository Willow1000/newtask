import copy

from common_action_framework.common_action_framework.reuse_action import update_action

 
from .Movement import Movement
"""
this class is a composite of movements, it will execute all the movements in the list
"""

class MoveComposition(Movement):
    def __init__(
        self,
        movementId: str,
    ) -> None:
        super().__init__(finalColor=None, initialColor=None, currentColorIndex=None, colorPatternSet=set(), movementId=movementId)
        self.moveToList: list[Movement] = []

    def addMovement(self, movement: Movement) -> None:
        self.moveToList.append(movement)

    def addAllMovements(self, movements: list[Movement]) -> None:
        self.moveToList.extend(movements)

    def getMovements(self) -> list[Movement]:
        return self.moveToList

    def move(self) -> list[dict]:
        out_list = []
        for movement in self.moveToList:
            temp_dict = movement.move()
            # update temp_dict jump according to out_list length
            updates = [
                {
                    "id": "check_for_final_color",
                    "jump": {
                        "step_num": str( len(out_list) + 1 ),
                    },
                }
            ]
            update_action(temp_dict, updates)
            out_list.append(temp_dict)
        return out_list
        # return copy.deepcopy( out_list )

    def moveTest(self) -> list[dict]:
        print("Testing composition")
        out_list = []
        for movement in self.moveToList:
            temp_dict_list = movement.moveTest()
            # update temp_dict jump according to out_list length
            updates = [
                {
                    "id": "check_for_final_color",
                    "jump": {
                        "step_num": str( len(out_list) + 1 ),
                    },
                }
            ]
            update_action(temp_dict_list, updates)
            out_list += temp_dict_list
        return out_list
        # return copy.deepcopy( out_list )



