import os
import sys
import time
import threading
from multiprocessing import Process, Queue


"""

"""


class RecordImageStruct:
    def __init__(
        self,
        filename,
        parser_execution_state,
        failure_bool=False,
        custom_path=False,
        is_service_off=None,
        new_is_permanent_screen_record_service_off=None,
    ):
        self.filename = filename
        self.failure_bool = failure_bool
        self.parser_execution_state = parser_execution_state
        self.is_service_off = is_service_off
        self.new_is_permanent_screen_record_service_off = new_is_permanent_screen_record_service_off

        self.id = self.filename
        self.custom_path = custom_path  # controls if the path is custom or not
        self.print_list = [
            self.filename,
            self.failure_bool,
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
