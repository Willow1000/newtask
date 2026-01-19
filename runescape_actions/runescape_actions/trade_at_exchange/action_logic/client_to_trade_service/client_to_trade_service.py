from abc import ABC, abstractmethod
import requests
from multiprocessing import Queue
import os
import sys
import json
import random
import threading 
import time
from twisted.internet import reactor, protocol
from twisted.protocols.basic import NetstringReceiver
from collections import deque
 
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional
from enum import Enum

projects_path = os.environ["CLIENT_MANAGER_PROJECTS_PATH"]
runescape_project_path = projects_path + "/runescape_actions"
sys.path.append(runescape_project_path)
from utility.utility import dictionary_readeable_print, load_raw_json_message_to_dict, parse_to_json, json_to_dict, replace_unset_with_none


"""
handles all requests to a trade service, on behalf of a client
# TODO: it would be great that this service can send a trade confirmation by id to the trade service, and the 
 trade service would connect to a database that stores all trades
"""


"""
the idea of this enum is is: 
    every trade state is initialized with WAITING_FOR_TRADE
    WAITING_FOR_TRADE -> tradeState is initialized in this state
    STARTING_TRADE -> after receiving request from client 
     (STARTING_TRADE state is the state in which a client reply that the trade is finally in progress is being awaited)
    TRADE_IN_PROGRESS -> after trade is started, it will take up to 4 hours for trade to be completed
     # after client has confirmed that the trade has started, the state transitions to this state, which is the wait state
      the client will periodically check wether the someone has bought/sold the item in the exchange yet or not, 
       whenever someone has, this state will transition to TRADE_COMPLETED or TRADE_FAILED
    TRADE_COMPLETED -> after trade is completed
    TRADE_FAILED -> if trade fails for some reason and is completed, or aborted
"""
class TradeStateEnum(Enum):
    WAITING_FOR_TRADE = 0
    STARTING_TRADE = 1
    TRADE_IN_PROGRESS = 2
    ALL_UNITS_TRADED = 3
    TRADE_COMPLETED = 4
    TRADE_FAILED = 5

class ErrorIdsEnum(Enum):
    MAX_TRADES = "MAX_TRADES"
    NO_AVAILABLE_TRADES = "NO_AVAILABLE_TRADES"
    NETWORK_ERROR = "NETWORK_ERROR"
     
# error strings
UNABLE_TO_WAIT_FOR_TRADE = "CANT GO BACK TO WAITING_FOR_TRADE STATE"
UNABLE_TO_START_TRADE = "CANT START TRADE"
UNABLE_TO_SET_TRADE_IN_PROGRESS = "CANT SET TRADE IN PROGRESS"
UNABLE_TO_FAIL_TRADE = "CANT FAIL TRADE"
UNABLE_TO_COMPLETE_TRADE = "CANT COMPLETE TRADE"


class TradeError(Exception):
    """
    exception for bad output received from the trade service
    """
    pass  


class TradeSetupError(Exception):
    pass


class MaxTradesError(Exception):
    pass

class NoAvailableTradesError(Exception):
    """
    exception for when there are no available trades to process
    possibly because no completed buy trades are available, and you want to set a sell trade
    """
    pass

class SendMessageNetworkError(Exception):
    """
    Exception for network errors when sending messages to the trade service.
    """
    pass


@dataclass
class TradeInfo:
    """
    Represents trade information using Python's dataclass.
    """
    service_id: Optional[str] = None
    status: Optional[str] = None  # e.g., "WAITING_FOR_TRADE", "STARTING_TRADE", "TRADE_IN_PROGRESS", "TRADE_COMPLETED", "TRADE_FAILED"
    trade_id: Optional[str] = None
    account_type:Optional[str] = None
    trade_type: Optional[str] = None  # "buy" or "sell"
    amount_traded: Optional[int] = None  # Amount of items traded, if applicable
    item_id: Optional[int] = None  # ID of the item being traded
    price_to_buy: Optional[int] = None
    price_to_sell: Optional[int] = None
    amount_to_trade: Optional[int] = None  # Amount of items to trade
     
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this dataclass instance to a dictionary.
        """
        return asdict(self)

    def update(self, other_trade_info: 'TradeInfo') -> None:
        """
        Updates current class fields from the other class fields.
        Only non-None values from other_trade_info will be used to update this instance.

        Args:
            other_trade_info: Another TradeInfo instance to get updates from
        """
        # Check if the input is a TradeInfo instance
        if not isinstance(other_trade_info, TradeInfo):
            raise TypeError("other_trade_info must be an instance of TradeInfo")

        # Get all field names from the TradeInfo dataclass
        for field_name in other_trade_info.__dataclass_fields__:
            other_value = getattr(other_trade_info, field_name)
            # Only update if the other value is not None
            if other_value is not None:
                setattr(self, field_name, other_value)
                 
 
class TradeProcessingClientForJson:
    """
    purpose of this class is to provide the whole communication to the remote trade service, and provide whatever 
     results the trade service serves back
    """
    def __init__(self, url):
        self.url = url

    def handle_error(self, received_msg: dict) -> None:
        error_id = received_msg.get("error", None)
        if error_id is None:
            return
        if error_id == ErrorIdsEnum.MAX_TRADES.value:
            error_msg = received_msg.get("error_msg", "")
            raise MaxTradesError(error_msg)
        elif error_id == ErrorIdsEnum.NO_AVAILABLE_TRADES.value:
            error_msg = received_msg.get("error_msg", "")
            raise NoAvailableTradesError(error_msg)
        elif error_id == ErrorIdsEnum.NETWORK_ERROR.value:
            error_msg = received_msg.get("error_msg", "")
            raise SendMessageNetworkError(f"Network error occurred: {error_msg}")
     
    def send_register_client(self, trade_info: TradeInfo) -> TradeInfo:
        url_append = "manage" 
        # trade_info.status = TradeStateEnum.WAITING_FOR_TRADE.name
        if trade_info.service_id is None:
            raise TradeSetupError("Service ID must be set before sending trade request")
        if trade_info.account_type is None:
            raise TradeSetupError("Trade status must be set before sending trade request")
        data = trade_info.to_dict()
        data["action"] = "register"
        res = self.send_message(url_append, data, request_type="GET")
        self.handle_error(res)
        trade_info = build_trade_info_from_dict(res)
        return trade_info

    def send_buy_trade_request(self, trade_info: TradeInfo) -> TradeInfo:
        trade_info.trade_type = "buy"  # ensure type is set to "buy"
        res = self.send_trade_request(trade_info)
        return res

    def send_sell_trade_request(self, trade_info: TradeInfo) -> TradeInfo:
        trade_info.trade_type = "sell"  # ensure type is set to "sell"
        res = self.send_trade_request(trade_info)
        return res

    def send_trade_request(self, trade_info: TradeInfo) -> TradeInfo:
        url_append = "manage" 
        trade_info.status = TradeStateEnum.WAITING_FOR_TRADE.name
        if trade_info.service_id is None:
            raise TradeSetupError("Service ID must be set before sending trade request")
        if trade_info.status is None:
            raise TradeSetupError("Trade status must be set before sending trade request")
        if trade_info.account_type is None:
            raise TradeSetupError("Account type must be set before sending trade request")
        # if trade_info.trade_type is None:
            # trade type doesnt really need to be set
            # raise TradeSetupError("Trade type must be set before sending trade request")
        data = trade_info.to_dict()
        data["action"] = "trade"
        res = self.send_message(url_append, data, request_type="GET")
        try:
            self.handle_error(res)
        except MaxTradesError as e:
            print(f"Expected error occurred: {e}")
            return ErrorIdsEnum.MAX_TRADES.value
        trade_info = build_trade_info_from_dict(res)
        return trade_info

    def send_trade_started(self, trade_info: TradeInfo) -> TradeInfo:
        """
        This function is called when the client has performed all the initial steps to start the trade.
        It sends a request to the trade service to indicate that the trade has started.
        """
        url_append = "manage" 
        trade_info.status = TradeStateEnum.STARTING_TRADE.name
        if trade_info.service_id is None:
            raise TradeSetupError("Service ID must be set before sending trade request")
        if trade_info.status is None:
            raise TradeSetupError("Trade status must be set before sending trade request")
        if trade_info.trade_id is None:
            raise TradeSetupError("Trade ID must be set before sending trade request")
        data = trade_info.to_dict()
        data["action"] = "trade"
        res = self.send_message(url_append, data, request_type="GET") 
        self.handle_error(res)
        trade_info = build_trade_info_from_dict(res)
        return trade_info

    def send_trade_in_progress(self, trade_info: TradeInfo) -> TradeInfo:
        """
        this is essential for an action that checks if a trade is already completed or not
        the server will return the trade info back if the trade is not completed yet
        """
        url_append = "manage"
        trade_info.status = TradeStateEnum.TRADE_IN_PROGRESS.name
        print(f"DEBUGPRINT[240]: client_to_trade_service.py:179: trade_info={trade_info}")
        if trade_info.service_id is None:
            raise TradeSetupError("Service ID must be set before sending trade request")
        if trade_info.status is None:
            raise TradeSetupError("Trade status must be set before sending trade request")
        if trade_info.trade_id is None:
            raise TradeSetupError("Trade ID must be set before sending trade request")
        if trade_info.amount_traded is None:
            raise TradeSetupError("amount traded must be set before sending trade request")
        data = trade_info.to_dict()
        data["action"] = "trade"
        res = self.send_message(url_append, data, request_type="GET")
        self.handle_error(res)
        trade_info = build_trade_info_from_dict(res)
        return trade_info

    def send_trade_failed(self, trade_info: TradeInfo) -> TradeInfo:
        """
        This function is called when the client has failed to complete the trade.
        It sends a request to the trade service to indicate that the trade has failed.
        """
        url_append = "manage" 
        trade_info.status = TradeStateEnum.TRADE_FAILED.name
        if trade_info.service_id is None:
            raise TradeSetupError("Service ID must be set before sending trade request")
        if trade_info.status is None:
            raise TradeSetupError("Trade status must be set before sending trade request")
        if trade_info.trade_id is None:
            raise TradeSetupError("Trade ID must be set before sending trade request")
        data = trade_info.to_dict()
        data["action"] = "trade"
        res = self.send_message(url_append, data, request_type="GET") 
        self.handle_error(res)
        trade_info = build_trade_info_from_dict(res)
        return trade_info
     
    def send_complete_trade(self, trade_info: TradeInfo) -> TradeInfo: 
        url_append = "manage"
        trade_info.status = TradeStateEnum.TRADE_COMPLETED.name
        if trade_info.service_id is None:
            raise TradeSetupError("Service ID must be set before sending trade request")
        if trade_info.status is None:
            raise TradeSetupError("Trade status must be set before sending trade request")
        if trade_info.trade_id is None:
            raise TradeSetupError("Trade ID must be set before sending trade request")
        if trade_info.trade_type is None:
            raise TradeSetupError("Trade ID must be set before sending trade request")
        data = trade_info.to_dict()
        data["action"] = "trade"
        res = self.send_message(url_append, data, request_type="GET")
        self.handle_error(res)
        trade_info = build_trade_info_from_dict(res)
        return trade_info

    def send_debug_request(self) -> Dict[str, Any]:
        url_append = "debug"
        data = {}
        res = self.send_message(url_append, data, request_type="GET")
        return res
     
    def send_message(self, url_append, data: dict, request_type):
        url = f"{self.url}/{ url_append }"
        headers = {
            "Content-Type": "application/json"
        }
        try:
            if request_type.upper() == "POST":
                response = requests.post(url, headers=headers, data=json.dumps(data))
            elif request_type.upper() == "GET":
                response = requests.get(url, headers=headers, data=json.dumps(data))
            else:
                raise Exception(f"Unsupported request type: {request_type}")
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
            replace_unset_with_none(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending trade request, cause: {e}")
            return {"error": ErrorIdsEnum.NETWORK_ERROR.value, "error_msg": str(e)}


class TradesOfInterestManager:
    """
    purpose of this class is to provide a simple local interface to the remote trade service, which is different
     from TradeProcessingClientForJson, which contains only the required methods to communicate and get useful results from 
      the remote trade service, this class, however, allows for a more abstract interface for a more simple use case 
       which is to grab abstract the trades, and simply grab the next trade of interest for ease of use
    this class is designed to constantly have a number of possible trades on cache and ready to be transitioned into an ongoing 
     trade
    """
    def __init__(self, url, max_size_of_trades_of_interest, account_type, bot_id):
        self.trade_processing_client:TradeProcessingClientForJson = start_json_client_to_trade_service(url)
         
        # load trades of interest at startup
        self.bot_id = bot_id
        self.trades_of_interest: dict[str, TradeInfo] = {}  # reminder that in python the dict class preserves insertion order
        self.max_size_of_trades_of_interest = max_size_of_trades_of_interest
        self.pending_items = deque()
        self.processed_keys = set()
        self.current_trade_id:str
        self.previous_trade_id:str = None
        self.previous_trade: TradeInfo = None
        self.initial_setup_completed = False
        self.access_lock = threading.Lock()
        self.condition_var_new_trade_incoming = threading.Condition(self.access_lock)
         
        self.register_trade_info = self.send_register_message(account_type, bot_id)
        trade_thread = threading.Thread(target=self.grab_trades_thread, args=())
        trade_thread.daemon = True
        trade_thread.start()

    def send_register_message(self, account_type, bot_id) -> TradeInfo:
        info_dict = {
            "account_type":account_type,
            "service_id":bot_id,
        }
        trade_info = build_trade_info_from_dict(info_dict)
        is_trade_info_setup = False
        while not is_trade_info_setup:
            try:
                trade_info_register_client = self.trade_processing_client.send_register_client(trade_info)
                is_trade_info_setup = True
            except SendMessageNetworkError as e:
                is_trade_info_setup = False
                wait_time = 10
                print(f"Network error occurred while registering trade info with trade service. possibly the trade service could not be reached for some reason. Retrying in {wait_time} seconds...")
                print(f"Error details: {e}")
                time.sleep(wait_time)
                continue
        print("trade info register response:")
        dictionary_readeable_print(trade_info_register_client.to_dict())
        print("trade client to trade service registered successfully. trade client to trade service should be able to function properly now")
        return trade_info_register_client 

    def get_trade_processing_client(self) -> TradeProcessingClientForJson:
        return self.trade_processing_client
     
    def add_trade_of_interest(self, key, value):
        self.trades_of_interest[key] = value
        self.pending_items.append((key, value))
     
    def remove_from_dict_by_trade_id(self, trade_id):
        if trade_id in self.trades_of_interest:
            del self.trades_of_interest[trade_id]
            # Remove from pending if it's there
            self.pending_items = deque((k, v) for k, v in self.pending_items if k != trade_id)

    def get_current_trade(self) -> TradeInfo:
        return self.trades_of_interest[ self.current_trade_id ]

    def next_trade(self):
        while not self.initial_setup_completed:
            time.sleep(10)  # wait for the initial setup to complete
            print(f"Waiting for initial setup to complete for trade manager with id: {self.bot_id}...")
        with self.condition_var_new_trade_incoming:
            if self.pending_items:
                key, value = self.pending_items.popleft()
                if key in self.trades_of_interest:
                    if self.previous_trade_id is not None:
                        self.previous_trade = self.trades_of_interest[self.previous_trade_id]
                    self.processed_keys.add(key)
                    self.current_trade_id = key
                    self.previous_trade_id = self.current_trade_id
                    self.condition_var_new_trade_incoming.notify()
                    return True
            else:
                print("No more items to process")
                return False
    
    def grab_trades_thread(self):
        while True:
            with self.condition_var_new_trade_incoming:
                while len( self.trades_of_interest ) >= self.max_size_of_trades_of_interest:
                    self.condition_var_new_trade_incoming.wait()
            with self.access_lock:
                trade_info = self.trade_processing_client.send_trade_request(self.register_trade_info)
                self.add_trade_of_interest(trade_info.trade_id, trade_info)
                if len(self.trades_of_interest) >= self.max_size_of_trades_of_interest:
                    self.initial_setup_completed = True
             
         
def start_json_client_to_trade_service(url) -> TradeProcessingClientForJson:
    trade_processor = TradeProcessingClientForJson(url)
    return trade_processor
 
 
def build_trade_info_from_dict(input_dict:dict) -> TradeInfo:
    """
    many fields are optional, service_id is not required, because an absctract trade info, relating to an item may exist
    the optional fields are there to support all the different trade types
    """
    # error = input_dict.get("error", None)
    item_id = input_dict.get("item_id", None)
    service_id = input_dict.get( "service_id", None )
    status = input_dict.get("status", None)
    trade_id = input_dict.get("trade_id", None)
    account_type = input_dict.get("account_type", None)
    trade_type = input_dict.get("trade_type", None)
    amount_to_trade = input_dict.get("amount_to_trade", None)
    amount_traded = input_dict.get("amount_traded", None)
    price_to_buy = input_dict.get("price_to_buy", None)
    price_to_sell = input_dict.get("price_to_sell", None)

    return TradeInfo(
        service_id=service_id,
        status=status,
        trade_id=trade_id,
        account_type=account_type,
        trade_type=trade_type,
        amount_traded=amount_traded,
        item_id=item_id,
        price_to_buy=price_to_buy,
        price_to_sell=price_to_sell,
        amount_to_trade=amount_to_trade,
    )


