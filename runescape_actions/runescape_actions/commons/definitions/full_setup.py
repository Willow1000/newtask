import os 
import sys

# ACTIONS_PROJECT_PATH: common action framework project
path = os.environ["ACTIONS_PROJECT_PATH"]
sys.path.append(path)

# CURRENT_ACTION_LIST_PROJECT_PATH: directory with all the actions to import
path = os.environ["CURRENT_ACTION_LIST_PROJECT_PATH"]
sys.path.append(path)

from runescape_actions.commons.move_to.action_logic.movementParser import (
    parseAllMovementFiles,
    parsecolor
    )

projects_path = os.environ["CLIENT_MANAGER_PROJECTS_PATH"]
runescape_actions_path = projects_path + "/runescape_actions"

map_of_possible_movements = {} # map of movementId to Movement object
map_colors = {}

MOVEMENT_DIR_PATH = runescape_actions_path + "/runescape_actions/commons/definitions/movements"

map_colors = parsecolor(runescape_actions_path + "/runescape_actions/commons/definitions/entity/color_map", map_colors)

print("Movement dir", MOVEMENT_DIR_PATH)
movements = parseAllMovementFiles(MOVEMENT_DIR_PATH, map_colors)
for movement in movements:
        map_of_possible_movements[movement.getId()] = movement.move()


