from basic_interaction import (
    get_action_picture_by_name,
    none_step_verify,
    get_test_picture_by_name,
)
from utility import dictionary_readeable_print
from reuse_action import merge_dicts, update_step, update_action
 

if __name__ == "__main__":
    #test
    step_0 = {
        "check": '',
        "verify": get_action_picture_by_name("report"),
        "test": [
            {
                "mock_image": get_test_picture_by_name("not_in_game_lobby"),  
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("test_lowbar")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "check_app_state_in_game_lobby", 
    }
    # Step 1: Click the screwdriver icon
    step_1 = {
        "check": get_action_picture_by_name("screwdriver"),
        "verify": get_action_picture_by_name("settings_menu_opened"),
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_screwdriver"),
                "replay_input": {"replay_type": "mouse", "coords": None}, 
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("ready_to_insert_npc")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "click_screwdriver_icon_step", 
    }
    # Step 2: Type "npc" in the search box
    step_2 = {
        "check": '',
        "check_args": {
            "write_string_in_client": {
                "string_to_write": "Npc", 
            },
        },
        "verify": get_test_picture_by_name("npc_inserted"),
        "test": [
            {
                "mock_image": get_test_picture_by_name("ready_to_insert_npc"),  # Mock image of the focused search box
                "replay_input": {
                    "replay_type": "keyboard",
                    "word_to_write": None,
                },
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("npc_inserted")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "xdot_keyboard_processing",
                "verify": "template_match",
            }
        },
        "id": "type_npc_in_searchbox_step",  # ID indicating this is the type "npc" in searchbox step
    }
    # Step 3: Click the gear icon next to NPC indicators
    step_3 = {
        "check": '',  
        "check_args": {
            "template_match_for_plugin_step": {
                "name": get_action_picture_by_name("name"), 
                "options_list": 'test', 
                "precision": 0.8,
                "offset": (146,0)

            },
        },
        "verify": get_action_picture_by_name("npc_settings_opened"), 
        "test": [
            {
                "mock_image": get_action_picture_by_name("npc_gear_icon"),  
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_action_picture_by_name("npc_settings_opened")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "click_gear_icon_step",
    }
    # Step 4: Click the npc name textbox
    step_4 = {
        "check": '',  
        "check_args": {
            "template_match_for_npc_step": {
                "npc_to_highlight_textbox": get_action_picture_by_name("npc_to_highlight_textbox"), 
                "npc_indicators_options": 'test', 
                "precision": 0.8,
                "offset": (0,18)

            },
        },
        "verify": get_action_picture_by_name("npc_textbox_focused"),
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_existing_textbox"),
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_action_picture_by_name("npc_textbox_focused")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "press_existing_user",
    }
    # Step 5: Type "Banker" in the textbox below NPCs to highlight
    step_5 = {
        "check": '',  
        "check_args": {
            "write_string_in_client": {
                "string_to_write": "Banker", 
            },
        },
        "verify": '',  # Verify "Banker" was written
        "test": [
            {
                "mock_image": get_test_picture_by_name("ready_to_insert_npc_name"),  # Mock image of the focused highlight textbox
                "replay_input": {
                    "replay_type": "keyboard",
                    "word_to_write": None,
                },
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_action_picture_by_name("banker_inserted_confirmation")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "xdot_keyboard_processing",
                "verify": "template_match",
            }
        },
        "id": "type_npc_name",
    }
    # Step 6: Click on the button next to NPC indicator
    step_6 = {
        "check": get_action_picture_by_name("npc_indicator_button"),
        "verify": get_action_picture_by_name("npc_plugin_on"),
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_existing_plugin"),
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("test_npc_plugin_on")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "press_existing_user",
    }
    # Step 7: Click on the button next to NPC indicator
    step_7 = {
        "check": get_action_picture_by_name("npc_indicator_button"),
        "verify": get_action_picture_by_name("npc_plugin_on"),
        "test": [
            {
                "mock_image": get_test_picture_by_name("test_existing_plugin"),
                "replay_input": {"replay_type": "mouse", "coords": None},
            },
        ],
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("test_npc_plugin_on")
            ],
        },
        "processor_info": {
            "processor_type": {
                "check": "template_match",
                "verify": "template_match",
            },
        },
        "id": "press_existing_user",
    }
    # final step, always add a final step, this is for the if else cases
    action_ordered_steps = [
        step_0,
        step_1,
        step_2,
        step_3,
        step_4,
        step_5,
        step_6,
        step_7,
        # always add final_step, this is for any need for an if-else statement
    ]

    updates = [
        {"id": "type_npc_name", 
         "check_args": {
             "send_npc_name_to_client": {
                 "npc_name": "Grand Exchange Clerk", 
             },
             'test': 123,
         },
         'verify': 'verify',
        }
    ]

    print('original steps')
    dictionary_readeable_print(action_ordered_steps)
    updated_steps = update_action(action_ordered_steps, updates)
    print()
    print()
    print('updated_steps:')
    dictionary_readeable_print(updated_steps)
    print()
    print()
    print('changes: updated_steps[5]')
    dictionary_readeable_print(updated_steps[5])

