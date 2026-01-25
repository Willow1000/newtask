example of bot status config:
{
    "jobs": {
        "target_accounts": ["bot2", "bot3", "bot4", "bot5"],
        "target_client_of_class_id": "rs",
        "sessions_metadata": {
            "update_type": "update",
            "is_looping_in_current_session": true,
            "changes_to_current_running_action_status": { 
                "step_num": 19,
                "current_running_state": "running"
                "temporary_session": "none",
            }, 
            "sessions": {
                "rs_login_session": [
                    {
                      "action_name": "rs_login",
                      "starting_step": -1,
                      "final_step": -1,
                      "is_looping_in_action": false,
                      "is_skipping_to_next_action": false
                    }
                ] 
            }
        }
    }
}

"changes_to_current_running_action_status" dictionary
 "current_running_state": this is how we stop/resume the service, the options are:
  "running", "stopped", "NA"(nothing changes)
   default value is "NA"
"is_looping_in_current_session": true, when true, the session will loop and not go to the next session
"sessions": a dictionary with constraints for specific actions within sessions
  "is_looping_in_action": if it is looping within this action
  "is_skipping_to_next_action": if it skips to the next action or just stops at the end of the current action, for a simple debugging
the temporary session is the session that can be started/stopped/toggled on top of the current session, example:
"temporary_session": {
   "job_id": "in_game_pause_job",
   "type": "toggle"
}, temporary session can be used to toggle a temporary job on/off, like in-game pause job, 
the job id is the predefined job it will use, the type is either "start_temp_session", "restore" or "toggle" 
check the: in_game_temporary_session_pause.json example 

notice that "is_looping_in_action" AND starting/final step together can be used to test specific steps in an action
