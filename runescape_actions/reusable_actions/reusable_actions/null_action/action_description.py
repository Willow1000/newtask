import os
import sys

# ACTIONS_PROJECT_PATH: common action framework project
path = os.environ["ACTIONS_PROJECT_PATH"]
sys.path.append(path)

# CURRENT_ACTION_LIST_PROJECT_PATH: directory with all the actions to import
path = os.environ["CURRENT_ACTION_LIST_PROJECT_PATH"]
sys.path.append(path)

time_limit = None  # time limit for this action (in minutes)
current_action_id = "none_action"
app_config_id = "NA"  # each action may require a different set of configs from the app itself
context = (
    "none_context"  # context to know what profile to use, what is this session related to, etc.
)
# doesn't restart when none_context is entered
#  restarts only when leaving none_context to another context

# purpose:
#  meant to be used in a new session (due to context changes only being checked across sessionss)
#  meant to temporarily stop the app
#  once another session is eventually chosen, that session will start and app in client will restart
#  notes:
#   doesn't immediately restart the app, only restarts once next session is chosen

# no meaning for these
all_failure_elements = {}
action_ordered_steps = {}
