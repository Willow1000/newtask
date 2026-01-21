this file has all the required information on how to work with the internal api, you do not have access to this api 
 and cannot access anything about this api, you only have access to the documentation

2.2
example function:
def random_movement_for_check_world_step(args):
    reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
    fn_args = args["args_by_func"]  # here you are fetching the 'check_args'/ 'verify_args' dictionary
    current_func_args = fn_args["random_movement_for_check_world_step"] # and here you have the argument by name
    seconds_to_wait = current_func_args["wait_in_cli_secs"]

    result_dict = {}  # this line and below we are creating a dictionary to output a specific step
    # the following functions all change result_dict in different ways
    random_mouse_movement(args, result_dict)
    client_wait(result_dict, seconds_to_wait)
    ignore_processor(result_dict)
    return result_dict  # this result is outputted into the processing side

the args arguments is: 
fn_args = {
    "reference_of_client_of_class": reference_of_client_of_class,
    "input_from_previous_elements": payload,
    "args_by_func": args_by_func,
    "update_info_for_step": update_info_for_step,  # this is meant to be a dict that is able to update the step
}

the return value of: random_movement_for_check_world_step, result_dict will return values for the processor 
 if the return value is a string: 
  # for a quicker processing, if a string is returned, it's because the developer wants to treat the 
   # the function as a function that just returns as if the developer sent a string in step field
 else if it is a dictionary:
  basic dictionary fields:
   "is_sending_to_processor": True/False in case you need to send anything to be processed you will have to set this to True
    default is False 
   "image_to_find_path_list" is a list of images you can set, they will replace the list of images you can set in the 'check' field
    every element of this list must be a string, however
   "send_back_to_cli": this is in case you want the processed message to be sent back to the client or not, 
    if False, this will mean the client will take a bit longer until it does something, it waits for a certain 
     amount of time before it sends back an image to the server
   every other element you can add in a step you can also add in these dictionary fields, and it will update them

 with this basic fields in mind, you can take a look at common_action_framework/common_action_framework/basic_interaction.py,
  this file contains the base functions of anything that uses the mouse (request_mouse_action) and keyboard (send_w), if you 
   search for these functions you will find other more simplified funtions that are meant to be useable
  custom mouse interactions:
   if you take a look at: in common_action_framework/common_action_framework/common.py
    notice that these will use the functions from the basic_interaction.py file
   u can press within the boundaries of a color with: left_click_highlighted, 
    and you can press on an image on screen with: left_click_template_match_for_step(this is what happens 
     when your 'check' field is a string, this is in this file in case you want to do something custom with it)
    always visit common.py to see the docs on these methods, check the docs and these methods's requirements at: 
     template_match_for_step_movement
     mouse_to_highlighted_area_movement

   pay attention when choosing the function because there are click functions and movement functions, anything with the naming 
    convention *_movement will NOT click anything on screen, it will just move the cursor there

   explaining basic dictionary fields for cursor movement: 
    click_type: example: "click" (left click), "right", "shift_right"
    coords_type = "singular" (when it's a single coordinate and not a bunch of coordinates to move the mouse along)
    the basic_interaction.py functions:  add_left_click_to_movement_request, add_right_click_to_movement_request, ...
     allow you to use these seemingly and will come up whenever you want to add a click  to a movement, example: 
       left_click_highlighted fn in common.py, 
    if you need to create any of these, just follow this pattern *_movement, and then the different click types (easier to use 
     and easier to manage)
     
 custom keyboard interactions:
  there are also a bunch of functions in this file for custom keyboard interactions, everything that uses 
   the send_w fn is quite self explanatory

 important functions:
  -client_wait function: especially useful function to set a wait period before the client sends the game image 
   back to the server in order to process the next step
    you can see an example of this functions in rs_login, step with id: "random_movement_for_check_world_step_8", 
     you can also create a wait step if you use the function: get_sleep_step, and use the output to 
      create a step in your action_description.py file
  -verify_after_checking_once: allows for the 'check' field to run one time before verifying and continueing to 
   the next step, use it whenever you want to run the 'check' field only once
  -get_action_picture_by_name in basic_interaction.py: get_action_picture_by_name and its variants, 
   this function will get a picture from your action folder: all_action_files/screenshots/action/ 
    UNLESS you name the photo all/something in your 'check' field, 
     in this case it will search for photos in runescape_actions/commons/0common_photos/ folder, you 
      can see an example of this in action: in_game_pause 

example using functions:
 step 8 in rs_login is a great example of the pattern you want to do when you are using 'check_args' and using a custom function 
  in the 'check'/'verify' fields
  example:
      step_8 = {
          "check": random_movement_for_check_world_step,
          "union_to_next": True,
          "check_args": {
              "random_movement_for_check_world_step": {
                  "wait_in_cli_secs": 1,
              },
          },
          (...)
       } 
      and the random_movement_for_check_world_step in common.py: 
        def random_movement_for_check_world_step(args):
            reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
            fn_args = args["args_by_func"]
            current_func_args = fn_args["random_movement_for_check_world_step"]
            seconds_to_wait = current_func_args["wait_in_cli_secs"]
            (...)
      in this example, notice how the 'check_args' are used by the function, to retrieve the arguments, the same is the case 
       for 'verify' and 'verify_args', it would work in the same way
 2.2.1 passing information from one step to another:
  using and populating "info_for_step" field, the next steps can access this "info_for_step" and use and manipulate whatever is 
   inside, so this is how you send arguments from one step to another, if you really want to send arguments to a specific 
    step, just add an index the same as that specific step id and then access it in that step

2.3 accessing the bot state: 
 every function can access the whole bot state, using:
  reference_of_client_of_class, input_from_previous_elements = get_common_args(args)
  reference_of_client_of_class: this is the client representation on the server, you can manipulate anything that is 
   running on the server and relates to this client, using this reference
  using: reference_of_client_of_class.get_running_bot_status() you can reach the most important part of 
   what is running server side, which is everything that relates to your created action (from your action_description file),
    you can reference your current running step, etc.
  most important things you can access:
    profile = reference_of_client_of_class.get_profile()  # explained below 
    bot_status = reference_of_client_of_class.get_current_running_bot_status()  # explained below
    running_bot_id = reference_of_client_of_class.get_id()   # general rule of thumb this is used when naming or indexing things
        
 2.3.2 profile and accessing the profile:
  to access the profile use: profile = reference_of_client_of_class.get_profile() 
   the profile is a class that will contain information on the app you are botting, in case of a game, you will have your 
    game account information here, along with anything else required to authentica and specific to a game account
  profile files: 
   get_account_type
   get_account_id
   get_account_name
   get_account_password
   profile specific for Runescape:
    get_current_in_use_world
    get_proxy
    
 2.3.3 accessing running bot status
  the most important things here are:
   the ability to change steps: 
    fetch_current_step_num()
    fetch_current_step(step_num) (returns a copy)
    set_step_by_number(step_num, step) 
    fetch_step_num_by_id(step_id) # returns the first one with that id, in case you have multiple (to get a specific one you have 
      # to understand the nomenclature of the steps)
    fetch_step_by_id(step_id)
    replace_step_by_id(step_id, step)
    ** these 6 functions above allow you to change steps if need be
    user_jump_to_step(step_num)
    ** the above function lets you manipulate the step number (useful, can also implement while loops with this ofc)
    fetch_current_state()
    set_current_state(state)  #possible states: ["running", "stopped"]
    ** the above 2 functions let you stop and resume the state of the bot, remember that if you stop the thing it will be hard 
     to start it again because it will not process next steps, so what you will probably have to do is implement a thread, to 
      start it back on, or request some special feature on the server that eventually turns it back on
    add_new_step(step_num, new_step)  # adds new step at step num
    ** the above function will help you add new all the new steps you require in the middle of your action
    


 Step id naming:
  in common_action_framework/common_action_framework/common.py:
  StepManipulator is a class that is going to fix the step id namings, such that for every action, or if you use the same step
   twice when creating another action or something (meaning the step would have the same id), it will make sure that the step id 
    is unique, meaning it will append a bunch of things to the step ids, this should always be used the same way it is used in 
     rs_login action
   
   
  

