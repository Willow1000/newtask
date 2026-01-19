from PIL import ImageGrab
from PIL import Image
import copy

from common_action_framework.common_action_framework.basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from common_action_framework.common_action_framework.image_matching_logic import (
    template_matching
)
from common_action_framework.common_action_framework.common import (
    left_click_highlighted,
    send_user_name_to_replay_in_client,
    send_pw_to_replay_in_client,
    send_tab_key_to_client,
    send_enter_key_to_client,
    random_mouse_movement,
    verify_after_checking_once,
)

from common_action_framework.common_action_framework.reuse_action import (
    update_action,
    update_step,
    merge_dicts,
)


from runescape_actions.commons.highlight_npc.action_description import get_action_ordered_steps as get_highlight_npc
from runescape_actions.commons.deposit_bank.action_description import (
    get_deposit_x,
    get_deposit_all
)
from runescape_actions.commons.withdraw_bank.action_description import (
    get_withdraw_x
)
from runescape_actions.commons.craft_bracelet.action_description import get_craft_bracelet
from runescape_actions.commons.move_to.action_description import get_move_to as get_move_to

all_failure_elements = {
    "send_creds": [
        get_action_picture_by_name("try_again_button")
    ],
}

time_limit = None  # time limit for this action (in minutes)
current_action_id = "crafting_gold_bracelet"
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.



action_ordered_steps = get_craft_bracelet("gold_bracelet", "gold_bar")
