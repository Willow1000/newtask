import os
import sys
import time
import threading
from multiprocessing import Process, Queue


class ReplayInputStruct:
    def __init__(
        self,
        xdo_instructions,
        element_to_find_path,
        screen_save_filename,
        parser_execution_state,
        finish_sequence_bool,
        is_service_off=None,
    ):
        self.xdo_instructions = xdo_instructions
        self.element_to_find_path = element_to_find_path
        self.screen_save_filename = screen_save_filename
        self.parser_execution_state = parser_execution_state
        self.finish_sequence_bool = finish_sequence_bool
        self.is_service_off = is_service_off

        self.id = self.xdo_instructions
        self.print_list = [
            self.xdo_instructions,
            self.element_to_find_path,
            self.screen_save_filename,
            self.finish_sequence_bool,
        ]

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __hash__(self):
        # necessary for instances to behave sanely in dicts and sets.
        return hash(self.id)

    def __str__(self):
        return str(self.print_list)
