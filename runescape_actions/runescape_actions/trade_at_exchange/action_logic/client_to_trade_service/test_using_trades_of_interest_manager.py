import os
import threading
import copy
import sys
import requests
import json
from client_to_trade_service import start_json_client_to_trade_service
from client_to_trade_service import TradeProcessingClientForJson
from client_to_trade_service import TradeInfo
from client_to_trade_service import TradeStateEnum
from client_to_trade_service import build_trade_info_from_dict
projects_path = os.environ["CLIENT_MANAGER_PROJECTS_PATH"]
runescape_project_path = projects_path + "/runescape_actions"
sys.path.append(runescape_project_path)
from utility.utility import load_raw_json_message_to_dict, parse_to_json, json_to_dict
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import TradesOfInterestManager
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import TradeStateEnum
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import TradeInfo
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import TradeError
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import MaxTradesError
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import ErrorIdsEnum
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import build_trade_info_from_dict
from utility.utility import dictionary_readeable_print


def thread_send_req(trade_manager, unique_trade_ids): 
    print(f"Trades of interest for trade manager with bot id: {trade_manager.bot_id}")
    for i in range(9):
        trade_manager.next_trade()
        current_trade = trade_manager.get_current_trade() 
        print(f"current_trade id: {current_trade.trade_id}")
        if current_trade.trade_id in unique_trade_ids:
            print(f"ERROR: Trade id {current_trade.trade_id} already exists in unique_trade_ids set.")
            sys.exit(1)
        unique_trade_ids.add(current_trade.trade_id)

 
if __name__ == "__main__":
    url = "http://localhost:5000" 
    print("REMINDER: you always need to manually start the server first on localhost:5000")
    max_size_of_trades_of_interest = 9
    account_type = "members"
    bot_id = "test_bot_id"
    trades_manager = TradesOfInterestManager(url, max_size_of_trades_of_interest, account_type, bot_id)

    max_size_of_trades_of_interest = 9
    account_type = "members"
    bot_id = "test_bot_id2"
    trades_manager2 = TradesOfInterestManager(url, max_size_of_trades_of_interest, account_type, bot_id)

    trades_managers_list = [trades_manager, trades_manager2]
    unique_trade_ids = set()
    thread_id_set = set() 
     
    for trade_manager in trades_managers_list:
        thread = threading.Thread(target=thread_send_req, args=(trade_manager, unique_trade_ids))
        thread.start()
        thread_id_set.add(thread)
     
    for thread in thread_id_set:
        thread.join()


