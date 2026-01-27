what is this for?
 defining a job:
 *a job is the composition of the metadata(where and how will it run) 
  and the session information(what the job does)

 the session data is just the static configuration of the job in the runescape_actions, 
  runescape_actions provides a number of static job configurations, afterwards we just 
   have to provide those configurations some metadata that tells where these jobs 
    will run and for how long, at what times of the day, etc., which is the files in 
     this directory exist, to provide this metadata

 a job is a configuration for a scheduler to send to the centralized manager, the scheduler 
  will schedule which times of day the jobs run most of all, will assign priority to jobs, 
   where the jobs will run, and this description will
    provide any required metadata for the jobs to run, this metadata will be  
     consumed by the scheduler, this configuration will mix with any required job 
      configuration in the runescape_actions jobs/ folder, but these configurations are 
       metadata for the configurations in the jobs/ folder, this metadata will be consumed 
        by the scheduler, but it can have many different formats, and ideally can be fine tuned 
         by any other tool, like a command line tool or something of the such, these jobs 
          in this directory are merged into the actual data dictionaries and sent as a  
           config to the centralized manager, and that is how manual/automated scheduling 
            works
  
 
what do these fields do? 
"jobs_to_run" this field is a dict of fields that will be appended to  
 one of the possible session specifications, tells the scheduler for how long to run 
  (run_time_seconds) and at what hours of the day to give a higher priority for this task to run
"target_accounts" this field is a list, but in reality, it's a range (it has 2 
 elements), and these elements, tell the range of the account ids that will be used

  all the accounts ids are represented in the profiles folder, with the all the information required 
   for every account

example:
{
  "target_accounts": ["bot2", "bot3"],
  "jobs_to_run": {
    "rs_login_job": {
      "run_time_seconds": 0,
    },
    "smithing_path_1_job": {
      "run_time_seconds": 1800,
      "list_of_start_time_hours_of_day": [10, 20],
    }
  },
}

"sessions_metadata" fields:
-"update_type":
 "reload" will reload the entire job configuration (creates a new running bot status), and info 
  will be lost on the previous running bot status, which can be just fine
 "update" will update the current running bot status, and info will be kept on the previous running bot status,
  any new added sessions will be appended to after the current sessions, and run after them
-"sessions": this permanently changes how a session will run, every time, until there is another update,
 however, no need to use this to change current action configs, cause you can use "changes_to_current_running_action_status" field 
  for that, this "sessions", it's meant to change things forever


"settings" are only settings changes and action changes, these settings dont propagate to clients, only to server side things

