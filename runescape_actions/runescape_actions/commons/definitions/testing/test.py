import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'runescape_actions'))
sys.path.append(os.path.join(os.getcwd(), 'LocallyAvailableActionTooling'))

from runescape_actions.commons.move_to.action_logic.movementParser import (
    parseFile,
    parsecolor,
)

projects_path = os.environ["CLIENT_MANAGER_PROJECTS_PATH"]
runescape_actions_path = projects_path + "/runescape_actions"

map_colors= {}

map_colors = parsecolor(runescape_actions_path + "/runescape_actions/commons/definitions/testing/colors.txt", map_colors)

if __name__ == "__main__":
    action_ordered_steps = parseFile(f"{runescape_actions_path}/runescape_actions/commons/definitions/testing/comp1.txt", map_colors).moveTest()
    print("Summary of test:")
    for step in action_ordered_steps:
        print("id:")
        print(step.get("id", "No ID"))

        if "check" in step:
            print("check:")
            print(step["check"])
        else:
            print("jump")
            print(step.get("jump", "No jump key"))

        print("verify:")
        print(step.get("verify", "No verify key"))

    
        print("\n")
