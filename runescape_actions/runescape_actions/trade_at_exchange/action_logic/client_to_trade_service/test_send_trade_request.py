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
from runescape_actions.trade_at_exchange.action_logic.client_to_trade_service.client_to_trade_service import build_trade_info_from_dict
 
from utility.utility import dictionary_readeable_print


if __name__ == "__main__":
    url = "http://localhost:5000" 
    print("REMINDER: you always need to manually start the server first on localhost:5000")
    trade_processing_client:TradeProcessingClientForJson = start_json_client_to_trade_service(url) 

    info_dict = {
        "account_type": "members",
        "service_id": "test_service_id",
    }
    trade_info = build_trade_info_from_dict(info_dict)

    trade_info_register_client = trade_processing_client.send_register_client(trade_info)
    print(f"Response to register: {trade_info_register_client}")

    print("INFO: Sending sell trade request... this request must fail, cause no completed buy trades exist yet")
    trade_info = copy.deepcopy(trade_info_register_client)
    has_error = False
    try:
        trade_info_temp = trade_processing_client.send_sell_trade_request(trade_info) 
    except Exception as e:
        has_error = True
        print(f"Expected error occurred: {e}")
    print(f"Response to initial trade request that must fail, and has it failed?: {has_error}")
    if not has_error:
        print("ERROR: Expected SELL trade without previous completed trade to fail, but it succeeded. TEST failed")
        print(f"the response from server was: {trade_info_temp}")
        sys.exit(1)

    print("INFO: Sending buy trade request...")
    trade_info = copy.deepcopy(trade_info_register_client)
    trade_info_result = trade_processing_client.send_buy_trade_request(trade_info)
    print(f"Response to initial buy trade request: {trade_info_result}")
    assert trade_info_result.status == TradeStateEnum.STARTING_TRADE.name
    assert trade_info_result.amount_to_trade == 1000
    assert trade_info_result.price_to_buy == 1000
    assert trade_info_result.trade_id is not None
    assert trade_info_result.trade_type == "buy"

    # trade started is a signal the client sends to the server to indicate it has performed all the initial steps to start the trade
    print("INFO: Sending trade started request...")
    trade_info = copy.deepcopy(trade_info_result)
    trade_info_result_trade_started = trade_processing_client.send_trade_started(trade_info)
    print(f"Response to send trade started for buy request: {trade_info_result_trade_started}")
    assert trade_info_result_trade_started.status == TradeStateEnum.TRADE_IN_PROGRESS.name

    # there will be an action that checks on if the item is sold yet or not
    print("INFO: Sending trade in progress request...")
    trade_info = copy.deepcopy(trade_info_result_trade_started)
    trade_info.amount_traded = 10
    trade_info_result = trade_processing_client.send_trade_in_progress(trade_info)
    print(f"Response to trade in progress after trading only 10 units: {trade_info_result}")
    assert trade_info_result.status == TradeStateEnum.TRADE_IN_PROGRESS.name

    print("INFO: Sending trade in progress request 2...")
    trade_info = copy.deepcopy(trade_info_result)
    trade_info.amount_traded = trade_info.amount_to_trade
    trade_info_result = trade_processing_client.send_trade_in_progress(trade_info)
    print(f"Response to trade in progress request, after everything is sold: {trade_info_result}")
    assert trade_info_result.status == TradeStateEnum.ALL_UNITS_TRADED.name
     
    is_complete = False
    if trade_info_result.status == TradeStateEnum.ALL_UNITS_TRADED.name or \
            trade_info_result.status == TradeStateEnum.TRADE_FAILED.name:
        print(f"all units have been traded, trade has status: {trade_info_result.status}")
        is_complete = True

    if not is_complete:
        print("ERROR: could not trade all units of this trade, trade has failed. TEST failed")
        sys.exit(1)
     
    # complete trade is after a trade has been completed
    print("INFO: Sending complete trade request...")
    trade_info = copy.deepcopy(trade_info_result)
    trade_info_result = trade_processing_client.send_complete_trade(trade_info)
    print(f"Response to completed buy trade: {trade_info_result}")
    assert trade_info_result.status == TradeStateEnum.TRADE_COMPLETED.name
    assert trade_info_result.amount_traded == 1000
         

    # SELL TRADE


    print("INFO: starting steps to a SELL trade, after the completed BUY trade")
    print("INFO: Sending sell trade request...")
    trade_info = copy.deepcopy(trade_info_register_client)
    trade_info_result = trade_processing_client.send_sell_trade_request(trade_info)
    print(f"Response to starting sell trade (sent sell trade request): {trade_info_result}")
    assert trade_info_result.status == TradeStateEnum.STARTING_TRADE.name
    assert trade_info_result.trade_type == "sell"
    assert trade_info_result.price_to_sell == 1010
    assert trade_info_result.trade_id is not None

    # trade started is a signal the client sends to the server to indicate it has performed all the initial steps to start the trade
    print("INFO: sending trade started signal...")
    trade_info = copy.deepcopy(trade_info_result)
    trade_info_result_trade_started = trade_processing_client.send_trade_started(trade_info)
    print(f"Response to send trade started for buy request: {trade_info_result_trade_started}")
    assert trade_info_result_trade_started.status == TradeStateEnum.TRADE_IN_PROGRESS.name

    # there will be an action that checks on if the item is sold yet or not
    print("INFO: Sending sell trade in progress request...")
    trade_info = copy.deepcopy(trade_info_result_trade_started)
    trade_info.amount_traded = trade_info.amount_to_trade
    trade_info_result = trade_processing_client.send_trade_in_progress(trade_info)
    print(f"Response to sell trade in progress: {trade_info_result}")
    assert trade_info_result.status == TradeStateEnum.ALL_UNITS_TRADED.name

    is_complete = False
    if trade_info_result.status == TradeStateEnum.ALL_UNITS_TRADED.name or \
            trade_info_result.status == TradeStateEnum.TRADE_FAILED.name:
        print(f"all units of the trade have been traded: {trade_info_result.status}")
        is_complete = True
    if not is_complete:
        print("ERROR: could not trade all units of this trade, trade has failed. TEST failed")
        sys.exit(1)
     
    # complete trade is after a trade has been completed
    print("INFO: Sending complete trade request...")
    trade_info = copy.deepcopy(trade_info_result)
    trade_info_result = trade_processing_client.send_complete_trade(trade_info)
    print(f"Response to sending complete sell trade request: {trade_info_result}")
    assert trade_info_result.status == TradeStateEnum.TRADE_COMPLETED.name
    assert trade_info_result.amount_traded == 1000

    out = trade_processing_client.send_debug_request()
    dictionary_readeable_print(out)

     

