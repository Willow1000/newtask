import os
import sys


"""
every function should accept a dictionary argument as input with all the arguments
functions can return other functions to serve as verification for the step they are on
"""

"""
specific functions only to be used in this action
"""

from common_action_framework.common_action_framework.common import (
    get_common_args,
    random_mouse_movement,
    client_wait,
)

from common_action_framework.common_action_framework.basic_interaction import (
    ignore_processor,
) 

def start_trade(args):
    """
    This function is used to add a client to the action logic.
    It returns a dictionary with the common arguments needed for the action.
    """
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    reference_of_client_of_class.trade_processing_client.send_trade_started()



