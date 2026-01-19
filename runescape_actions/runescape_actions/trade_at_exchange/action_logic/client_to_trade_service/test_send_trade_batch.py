
import os
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
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import TradeStateEnum
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import TradeInfo
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import TradeError
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import MaxTradesError
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import ErrorIdsEnum
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import build_trade_info_from_dict

from utility.utility import dictionary_readeable_print

def send_number_new_trades_batch(batch_size, trade_info_result_list, trade_info_register_client): 
    for counter in range(batch_size):
        print("requesting trade")
        trade_info_result = trade_processing_client.send_trade_request(trade_info_register_client)
        if trade_info_result == ErrorIdsEnum.MAX_TRADES.value:
            print("ERROR: number new trades exceeds maximum allowed trades")
            continue
        print(f"DEBUGPRINT[254]: test_send_trade_batch.py:42: trade_info_result={trade_info_result}")
        # This is just to test the debug endpoint
        # It should return the current state of the trade info
        trade_info_result_list.append(trade_info_result)


def send_complete_trades_batch(batch_size, trade_info_result_list): 
    for i in range(int(batch_size)):
        print("sending complete trade")
        trade_info = trade_info_result_list[i]
        trade_info = trade_processing_client.send_complete_trade(trade_info)
        trade_info_result_list[i] = trade_info

 
def send_trade_in_progress_batch(batch_size, trade_info_result_list):
    for i in range(batch_size):
        print("sending trade progressing")
        trade_info = trade_info_result_list[i]
        if i >= TOTAL_NUMBER_TRADES - TRADES_OFFSET:
            # TRADES_OFFSET number of the trades are not completed
            trade_info.amount_to_trade = 10
        trade_info.amount_traded = trade_info.amount_to_trade
        trade_info = trade_processing_client.send_trade_in_progress(trade_info)
        trade_info_result_list[i] = trade_info


def send_trade_started_batch(batchsize, trade_info_result_list):
    for i in range(batchsize):
        print("sending trade started")
        trade_info = trade_info_result_list[i]
        trade_info = trade_processing_client.send_trade_started(trade_info)
        trade_info_result_list[i] = trade_info
     

if __name__ == "__main__":
    url = "http://localhost:5000" 
    print("REMINDER: you always need to manually start the server first on localhost:5000")
    trade_processing_client:TradeProcessingClientForJson = start_json_client_to_trade_service(url) 

    client_register_info_list = []
    for i in range(2):
        info_dict = {
            "account_type": "members",
            "service_id": f"test_service_id{i}",
        }
        trade_info = build_trade_info_from_dict(info_dict)

        trade_info_register_client = trade_processing_client.send_register_client(trade_info)
        client_register_info_list.append(trade_info_register_client)
        print(f"Response to register: {trade_info_register_client}")

    trade_info_result_dict = {}
    NUMBER_TRADES = 10
    TOTAL_NUMBER_TRADES = (9 if NUMBER_TRADES > 10 else NUMBER_TRADES)
    TRADES_OFFSET = 3  # number of trades that will not be comepleted
    for trade_info_register_client in client_register_info_list:
        trade_info_result_dict[trade_info_register_client.service_id] = []
        trade_info_result_list = trade_info_result_dict[trade_info_register_client.service_id] 
        print(f"trades for: { trade_info_register_client }")
        send_number_new_trades_batch(NUMBER_TRADES, trade_info_result_list, trade_info_register_client)
        send_trade_started_batch(len(trade_info_result_list), trade_info_result_list)
        send_trade_in_progress_batch(len( trade_info_result_list ), trade_info_result_list)
        send_complete_trades_batch( TOTAL_NUMBER_TRADES - TRADES_OFFSET , trade_info_result_list) 
         

    print("sending next phase of trades")
    # finish up the rest of the trades from both clients
    NUMBER_NEW_TRADES = TRADES_OFFSET
    trade_info_result_fixed_dict = {}
    for trade_info_register_client in client_register_info_list:
        trade_info_result_fixed_dict[trade_info_register_client.service_id] = []
        trade_info_results_fixed = trade_info_result_fixed_dict[trade_info_register_client.service_id] 
        trade_info_result_list = trade_info_result_dict[trade_info_register_client.service_id] 
        print(f"trades for: { trade_info_register_client }")
        send_number_new_trades_batch(NUMBER_NEW_TRADES, trade_info_results_fixed, trade_info_register_client)
        send_trade_started_batch(NUMBER_NEW_TRADES, trade_info_results_fixed)
        number_old_trades_to_complete = 0
        for i in trade_info_result_list:
            if i.status != TradeStateEnum.TRADE_COMPLETED.name:
                trade_info_results_fixed.append(i)
                number_old_trades_to_complete += 1
        TOTAL_TRADES_COUNTING_THE_NEW_TRADES = NUMBER_NEW_TRADES + number_old_trades_to_complete
        TOTAL_TRADES_COUNTING_THE_NEW_TRADES = (9 if TOTAL_TRADES_COUNTING_THE_NEW_TRADES > 10 else TOTAL_TRADES_COUNTING_THE_NEW_TRADES) 
        print(f"number of trades being completed: {TOTAL_TRADES_COUNTING_THE_NEW_TRADES}, should be the new trades:{NUMBER_NEW_TRADES} + the old uncompleted trades: {number_old_trades_to_complete}")
        send_complete_trades_batch(TOTAL_TRADES_COUNTING_THE_NEW_TRADES, trade_info_results_fixed)

    out = trade_processing_client.send_debug_request()
    dictionary_readeable_print(out)
         

