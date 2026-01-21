common actions that is meant to be used in whatever app you want
 different from: code common to all actions already in common_action_framework

guide on how the action_description works what fields to use etc. - this is in runescape_actions/README.md

1
1.1 examples creating common functionality
HOW TO CREATE A SIMPLE IF statement:
 use the 'jump' field for conditional jumps
  example:  rs_login step with id: "loop_until_login_successful"
HOW TO CREATE A LOOP: 
 use the 'jump' field as well
  example:  rs_login step with id: "loop_until_world_selected" 
HOW TO CREATE A REUSABLE FUNCTION:
 you need to create an action and then re import that action in another action (to reuse it as a function), 
  actions that have uses go into runescape_actions folder, however, actions that are to be only used as functions, 
   must go into runescape_actions/commons
  example: 
   in_game_pause and a reusable action: press_anywhere_in_menu this separation is created because I predict 
    more action will want to use press_anywhere_in_menu 
  
1.2 HOW TO TAKE A SCREENSHOT(using the custom screenshot tool):
 in runescape_actions/README.md: take a look at 1.3.2 quick guide on how to take screenshots

1.3 all_failure_elements dictionary:
 this is one of the last development phases, you can see the development phases in: ( section III.1 )
 purpose of this is to error handle possible problems
 the failure elements are ran through sequentially 
example: 
all_failure_elements = [
    "send_creds": { # for example this failure element is meant to be checked in case any step fails
        # so, after a step fails, the system will look for this image, and go back to step_11 (step with id: send_creds) 
        #  if it finds it
        "session": "NA",  # default is "NA" it means it's a step id from the current session
        "level": "normal"  # default is "normal", this check is always ran through
         # also have "last-resort" which is can only exist one, it's the thing that the bot will do if everything else fails,
          # if that fails too all that can be done is log and disconnect
         # last-resort will always log what happened
        "images": {
            "id1": [ 
                "image": get_action_picture_by_name("try_again_button"),
                "processor_type": "template_match",
            ],
        },
    },
]

what this example means is that whenever the system thinks there is a problem in a step, ex. because the 'check' field is not found 
 multiple times, what happens is that the screenshot "try_again_button" is searched on screen and if it is
  found it goes to the step which id is: 'send_creds'
 you should always have the least possible amount of failure_elements, and NEVER replace loops 
  with failure elements, remember that failure_elements will ALL be checked if the system thinks there is some sort of failure
 an example of a last-resort failure element to have is probably to return to initial state, in case of runescape that's probably 
  teleporting back to the place where you can restart the task

1.4 explaining the standalone fields in an action (these are elements not specific to any step or all the steps)
the following elements in any action:
time_limit = None  # time limit for this action (in minutes)
this is in case the action is possibly flawed, should always be set (after testing), this feature 
 is currently not implemented BUT always remember to set it to make sure the bot doesnt malfunction and 
  gets stuck somewhere forever, when the time runs out it is supposed to go to failure elements

THIS MUST ALWAYS BE CHANGED
this is the current action id, should always change and match the name of the name of the directory 
 you chose to name, never forget to change this
current_action_id = "rs_login" 

the app config to use:
app_config_id = "full_rs"  # each action may require a different set of configs from the app itself
 this needs to be properly analysed, full_rs is the default, leave that as is, and this will be changed as required

always leave the context as is unless you know what you are doing
context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.


1.5 explaining all elements in a step:
 the list of all actions
steps:
 remember that as you are doing the steps you need to provide the step description as explained in 
  the runescape_actions/README.md file
     several "check" or "verify" fields: this allows for more than a single possibility when resolving actions, you can have:
     "check1", "check2", ... starting with the word: "check" in the field
     "check_resolution_type": this field relates to the ordering of how the several fields starting with the same name will be 
      processed, "random" is for a random ordering of which "check" field will be first, and the default "ordered", which is 
       for the defined order in the dictionary, this ordering refers about what was mentioned above, the "check", "check1", "check2"
     "check_resolution_method": "once" means it just returns found or not found, and only does one of the check fields, 
       the first one it can
       "first_match" means it goes through all the check fields until it finds one that is acceptable, if none is found, will 
        return the fail to the client, default is: "first_match"
      example:
      "info_for_step": {
          "send_back_to_cli": False,
          "is_waiting_for_cli_to_proceed": False,
      },
      'send_back_to_cli': by default this field is always True, meaning that at every step the server 
       sends to the client the information processed for that step, however, when setting this to False,
        the server won't be sending back any information, 'union_to_next' also sets this to True, this 
         is in case you want to process a bunch of steps in a row on the server before sending them back 
          to the client, this will be much faster, you will probably want to use 'union_to_next' field 
           most of the times, and only fine tune with this setting when writting a custom function
      'is_waiting_for_cli_to_proceed': by default always True, meaning that at every step it always 
       wait to send the info back to client and answer from the client to procceed to the next step,
        in case it's set to false, it will immediatly procced to the next step
      is_waiting_for_cli_to_proceed and send_back_to_cli are separated because you may want to process 
       this step without sending info back to client, however, not want to procceed to the next step, 
        or vice versa
     you can update this 'info_for_step' from a custom function, anytime, however, the info for step 
      will permanently be associated to that step, so this is used ONLY as in 
       the example, those fields mentioned above must be changed here, OR when creating a function, 
        (this the changeable part of a step), meaning from a different step or a different action 
         you can change this step's info_for_step field, keep in mind that it is changed permanently 
     "info_for_step" is also a way to send information forward from current step to the next, a function in step 3 could populate 
      info_for_step and it would propagate for a step further ahead in step 8, the function in step 8, would ideally delete 
       this data sent from step 3 such that it wouldnt stay in this info_for_step dictionary forever, basically any step anywhere
        can access and change what is inside this "info_for_step" dictionary
    -'check' the element that is going to be used to perform an action on the server,
     IF this element is a STRING it's meant to be an image path, and it will be used to find the 
      the image in that path and see if it exists on the received image
     IF this 'check' field is a function (pointer to function), it will call this function on the server 
      and do whatever you tell the function to do, make sure you set 'check_args' field for the function 
       arguments
     IF this element is a list, (it can be a list of functions or strings), it will just sequentially 
      run the check elements as it would if you were to pass a bunch of steps, ideally you do stuff 
       in a bunch of steps, unless it doesnt make sense to do so, like sending a bunch of keyboard keys
        in a row, can be done like this, however, sending a bunch of strings in a list is highly 
         impratical
     'check_args' is the arguments to all the functions (if a list) in the 'check' field, 
      this field is a dictionary, therefore, 
       when creating a function you have to make sure it received a single argument, and that argument 
        must be a dictionary (inside that dict, all the args you want to set)
    -'union_to_next': "glues" current step to the next step
     (meant to make it easier) to code,
      no need to use the 'verify' field in the current step, however,
       after the previous step is verified,
        the next step is always verified as well,
         therefore, "union_to_next" always sets the 'verify' field to
          verify_after_checking_once function,
           'union_to_next' is an optional field,
            that changes the 'verify' field if set, its purpose is to fix the case mentioned above, 
             in case you want to have a bunch of 'check' fields in a row, you should use this 
              (unless they are a bunch of functions, in that case you should just use a 
               list in the 'check' field, but if it's a series of photo names, you should use this, 
                to make it more readeable)
    -'verify' list of strings (screenshot names) to verify after all 'check' elements have been processed
     (verifying happens after the previous 'check' elements have been processed
      and before the next step is processed), in its default verify mode all
       elements in list must be verified, not just one
     this 'verify' field works a lot like the 'check' field, this field allows for both string, 
      and functions, also allows for a list of these, just like with the 'check' field

   1.5.2 multiple action possibilities and the 'check'/'verify' fields:
    *this is great whenever there is more than a single possible way to do something, to involve variety and avoid 
     bot detection, you can also multiple possibilities, or simply to allow to press  more than a single image on screen,
      in case all the pressed images do the same
     a great thing here is: you can set to pick a random of the fields (can pick one of "check1", "check", "check3", ...), 
      OR you can process them sequentially until the first one is found
    multiple "check"/"verify" fields: this allows for more than a single possibility when resolving actions, you can have:
     "check1", "check2", ... starting with the word: "check" in the field
    "verify_resolution_type": this field relates to the ordering of how the several fields starting with the same name will be 
     processed, "random" is for a random ordering of which "check" field will be first, and the default "ordered", which is 
      for the defined order in the dictionary, this ordering refers about what was mentioned above, the "check", "check1", "check2"
    "verify_resolution_method": "once" means it just returns found or not found, and only does one of the check fields, 
      the first one it can
      "first_match" means it goes through all the fields until it finds one that is acceptable, if none is found, will 
      return false
      default is: "first_match"
     
    -'verify_mode': different modes to verify the image,
     *verify_once*: verification step is true if at least
      one of the images in the 'verify' field list
       is found
     *verify_all*: requires all images to be found, default is verify_all, optional field
    keep in mind "verify_mode" can be used together with "verify1", "verify2", ...., and the "verify_resolution_type" and the 
     "verify_resolution_method"
     
    -'verify_args' dict with input for the functions in 'verify',
     optional
    info_for_step
    -'reverse_verification': just reverses the verification, it's essentially a 'NOT'
     
    -'jump': behaves as a conditional jump, is a dict that
     requires the inner fields:
      -'verify', works similar to previous verify (but needs to
       be inside of the jump field), this field is to verify if the jump condition appears or not, 
        therefore, this is a conditional jump, if the condition in 'verify' field is true this field will jump to 'step_num'
      -'step_num' to know where to jump if the
       condition/photo in 'verify' field is
        not true/ does not exist, requires the 'verify'
      -'reverse_verification': (true/false field)
       same as the 'reverse_verification' in the 'verify' field as explained above
      -fields inside the 'jump' dict, can also use all previous
       fields associated with the 'verify' field
        ('verify_mode', etc.),
      -if the 'verify' or
       'check' field outside 'jump' exist, they are
        ignored, a step with the jump field, only does the jump
     
    -'processor_info' dictionary with input for the processor and specified chose processor as well,
     will always contain the 'processor_type' element,
      there is no default for this, by design, NOT optional
      'processor_type': for the 'check' and 'verify' elements
       example:
        "processor_type": {
            "check": "template_match",
            "verify": "template_match",
        },
        options for the type of processor include: 
        'template_match' (finding an image inside another image),
        'xdot_keyboard_processing': (a specific type of keyboard processing, in case you want 
          to send keys back to the client, so the bot can replay them, this is the processor to use),
           you can see an example of using this in the rs_login
      this processor_info also accepts specific 'check_args' and 'verify_args', each of these fields are
       a list of dictionaries, each element in the list corresponds to an element in the list of 'check' 
        or 'verify', in case these are lists too, these args control how the processor will act when 
         processing a specific element of 'check' or 'verify' fields, this is sometimes required,
          these fields will always have defaults, however, depending on the screenshot or step, 
           they may need to be lowered
         example (from rs_login action):
          "verify_args": [
              {
                  "precision_required": 0.65,
              },
          ],
          'precision_required': this field controls what is the precision required for the server 
           to say that the icon image exists in the background image (in this example to say that 
            the 'verify' field image exists in the end_mock_image_list screenshot), this example is 
             in the rs_login action, check the comments there to see why it was required in this 
              specific step
         the same can be done for 'check_args' inside 'processor_info' field, remember that these 
          'check_args' and 'verify_args' are different than those you can use in the base dictionary 
           of the step, the args in this example have the same name, however, only have use inside 
            the 'processor_info' dictionary
     
    -'replay_info' dictionary this field is the field that provides info for the server to know 
     how will the server process information back to the client
       example of all possible fields in 'replay_info'
        "replay_info": {
            "click_info": {
                "click_type": "click", (defaults to 'click')
                "number_clicks": 1, (defaults to 1)
                "click_delay": 1, (defaults to None)
            },
        },
        'click_type': 'click'(to actually click the element on screen (left click))
          'none' to just move the cursor and not click any elements (default)
          'right': right click
        'number_of_clicks': number of followup clicks
        'click_delay': click delay in seconds, in case you want to add a delay, or None(default)
     
    -'id': is MANDATORY if there is a 'failure element' in this step, it's very useful
     
    -'cacheable' element (if it is cacheable for other bots, is everyone going to press that place 
     True/False, it's just a cache, if set to True all other bots willp press that place on screen, u
      must think hard if this is applicable or not), default is False
     reminder: pressing the same place on screen, doesnt actually mean pressing the same place on screen, there is always a 
      slightly built in offset in the endpoint of a movement, the bot doesnt allow pressing a place on screen with certainty,
       it ALWAYS offsets the place you click on slightly, therefore most things require error correction, this element specifically 
        was created to always be paired with a failure_element (in all_failure_elements) list (you can learn more about this 
         below)
    
    -'cacheable_time': has a default value, but you can change it, (in seconds)
     
    -'error_limit' count of the max number of errors, in case you want to change the 
     max number of errors for a given step, this are the max number of errors until searching for an 
      image in the failure_elements happens, this has a default value, almoust never will want to be changing this

    -'color_type': this is the color the image will be turned to before template 
     matching, colors are: "colored", "black_and_white", default is black and white
      you must pay very close attention to these whenever you are matching na item whose color matters, it's very easy 
       to forget this because the default is black and white and it works most times, but you will be wanting to change this 
        every time images you are searching for are too closely related, example: some item icons will look the same, HOWEVER, 
         they will not have the same color, in this case "colored" must be used

    -'cli_wait_secs': client waits for the 
      performed action on the client side before it sends the next image to the server, this is quite 
       useful in case you want to wait a couple seconds for an action to be performed on the client side without 
        sending the image back to the server, it may even optimize everything as the client will not 
         be sending any unnecessary images to the server if you do this correctly (in seconds)
      this can also be set in a custom function with: client_wait function in common.py

    1.5.2.2 multiple action possibilities and get_action_picture_by_name using 0common_photos images
     example using multiple action possibilities:  
     the "check"/"verify" elements will grab the path of the photos you send as argument to: 
      get_action_picture_by_name, they will look inside the action folder: all_action_files/screenshots/ , HOWEVER, 
       if the path of the screenshot starts with: all/ , it will instead be searched in another folder, a folder 
        with many commonly used photos, the folder is: common/0common_photos/* you can see this in the example action:
         in_game_pause, and its sub action it uses: press_anywhere_in_menu the following snippet:
       step_to_press_anything_in_menu_at_random = {
           "check": get_action_picture_by_name("all/dashboard/menu/account_management"),
           "check2": get_action_picture_by_name("all/dashboard/menu/character_summary"),
           "check3": get_action_picture_by_name("all/dashboard/menu/chat_channel"),
           "check4": get_action_picture_by_name("all/dashboard/menu/combat_options"),
           "check5": get_action_picture_by_name("all/dashboard/menu/emotes"),
           ( ...  )
       }
       here we can see the image naming convention
     
   1.5.3 test information:
    -'test': used to test the action step by sending a 'mock_image' to the server, 
     then receiving back coordinates and testing them against 'replay_input' (tuple) field
      inside this 'test' field (the image under 'mock_image' field is tested against the 'check' field),
       this field is always a list, because you can have more than one test, in the logs after running 
        the more extensive discord test you will see where the client pressed, this information is 
         a RED cross in the target given by the 'check' field and this target is drawn on the 
          'test' field's 'mock_image' fields
      example of a 'test' field
          "test": [
            {
                "mock_image": get_test_picture_by_name("screen_with_all_worlds"), (image to test the 'check' field against)
                "replay_input": {
                    "replay_type": "mouse", 
                    "coords": None,
                },
            },
          ],
          'replay_type': this field can be 'mouse' expects the replay on the client to be 'mouse':
           'replay_type' is 'mouse' you need to have a 'coords' field
            this is here for reference, but basically you always leave it at None for simplicity:
            this 'coords' field is the:
             expected coordinates returned to the client from the server for this test, these are the 
              coordinates where the 'check' field image is on the 'test' image, if this field is None, 
               then the expected value of the coords will be the same as ran in the previous test iteration,
                every 'test' field always runs for multiple iterations, when this field is set to None, 
                 the expected coords for the 2nd iteration will be within a range of the coords within 
                  the first iteration of when the test was ran
          'replay_type' can be 'keyboard' in this case the expected output back to the client is 
           a word, not a mouse movement (with coordinates), therefore, when the field is 'keyboard' a 
           'word_to_write'  field is expected, if set to None, this works the same way as above,
            if set to a word the test will make sure the returned word to write on the client is 
             the same word as in this field
          you will probably always want to leave these 'word_to_write' and 'coords' fields as None, 
           this is because the more extensive discord test was made as to test every step with multiple 
            iterations and setting these to None is just fine and faster
         'replay_type': 'NA' some steps dont require the test output to be checked, setting to 'NA' will skip that
         example of a 'test' field for keyboard:
          "test": [
              {
                  "mock_image": get_test_picture_by_name("ready_to_insert_password"),
                  "replay_input": {
                      "replay_type": "keyboard",
                      "word_to_write": None,
                  },
              },
          ],
          cant really test keyboard input, it's not simple, just test it live, and REMEMBER sometimes the inputs FAIL
    -'extra_test_info': this field was created to test the "verify" field and the "jump" fields,
       'end_mock_image_list': this field is a list with any amount of strings as picture names, 
        get_test_picture_by_name will get a picture from your screenshots/test/ directory and this 
         field is meant to test if the 'verify' field exists in any of these picture, in the logs 
          after the more extensive discord test, the green crosses will correspond the target of 
           the 'verify' field drawn up the picture in the 'end_mock_image_list' field
      to test the verify field, example:
          "extra_test_info": {
              "end_mock_image_list": [
                  get_test_picture_by_name("test_existing_user"),
                  get_test_picture_by_name("rs_app_requires_update"),
              ],
          },
      if you dont set this field, the default way to test the 'verify' field is it automatically checks the 'test' field of the next step 
       this means you can add a 'test' field to the final step in order to constantly test the 'verify' field
      to test the 'check' field, you can just add a 'test' field
      to test a 'jump' field:
       another way to use 'extra_test_info' field is when testing loops (alongside the 'jump' field),
        example:
        "extra_test_info": {
            "loop_info": {
                "num_iterations": 2,
                "img_after_loop": get_test_picture_by_name("test_verify_world_308_pressed"),
            },
        },
        in this example: 'loop_info' is used to test the loop, no more fields are required for 
         the 'verify' or 'check' fields, because there is None, 
          there is only the 'jump' field in this step and to test this 'jump' field this is how it's done,
           the 'loop_info' takes all the required information to test the loop, 
            'num_iterations': the number of iterations you are testing this loop for, (remember that 
             any test should have less than 6.5 minutes) 
            'img_after_loop': the image to send to end the loop, this image will be tested against 
             the 'jump' field's 'verify' field (double check the 'jump' field docs above to remember),
              the loop step still accepts a 'test' field, (the image that will be sent every iteration 
               the loop gets to this step (for an iteration number < 'num_iterations'))
          this is meant to be used alongside the "test" field, the idea is: 
           the "test" field will leave information of testing the "check" field, and the "img_after_loop" field will 
            provide information of where the "verify" field inside the "jump" will be pressing after the jump has been made
 
1.5.4 final step in every action: 
 final_step, make sure to add a final_step that does nothing in every_action you create,
  this is because you may want to jump to the end of the action at any time, or from another action to the 
   end of this action, always adding a final_step, allows for this, unless you really dont want this 
    behavior to be possible, this is always the same, except that the id MUST always be different, if you forget to change the id, 
     you will be breaking a lot of functionality, and introducing a bug
  it should look something like this:
   final_step = {
       "check": none_step_verify,
       "verify": none_step_verify,
       "id": "rs_login_final_step",
       "processor_info": {
           "processor_type": {
               "check": "template_match",
               "verify": "template_match",
           },
       },
   }
   (the bare minimum of a step)


1.6 common step structure patterns
 1.6.1 awaiting for an expected UI change to make a decision
 whenever there is a jump step you have to be careful, must wait because a jump step(next step) instantly jumps, problem is:
  if the UI hasnt updated accordingly yet on the client(and the client sends a screen that's not updated because for some reason 
   there is a delay between the client's action of pressing something on screen and the screen updating), this would ignore the 
    if clause, which is a common problem, an easy fix for this is in: rs_login step id: 
      await_by_verify_on_all_images_a_change_in_UI_is_verified_before_making_jump_decision 
      and the next step, which is a jump, however, these two work together to achieve the final result, which is:
       awaiting an expected change on the UI and then performing a decision(which is the next step's jump)
  and this is a common example of awaiting until the image exists and then using the image in a decision
 1.6.2 reusing an action in another action
  a good example is in: cooking_raw_swordfish action, an action whose test is working and that you can run
   in this action: you are using a function: get_cook_fish, if you search for this function, it is in an action that is ready 
    to be reused, every time you want a reusable action, you will follow this type of pattern
  the update_action function being the most important function here:
   it receives the updates list in cooking_raw_swordfish/action_description.py and applies the update to every element with the id 
    of the element of the list, it changes everything you provide to the step with that id


considerations:
    ALWAYS PUT THE 'FAILURE' ELEMENTS at the start even if they are empty for now, remember to write this down in action_explained file
    always remember to set action_id correctly, it must be unique
     "action_id1", "action_id2", these action ids are unique, there are comparisons, that compare for the start of the string, 
      and the above ids would be an example of doing it wrong
    make sure to create the steps in a readeable way, make sure you dont put all checks in a list 
     to save work
    in any action_description, the steps start at step 0, NOT step 1 (index on the list, and the name of the step should be the same, 
     to avoid bugs, cause sometimes the action list needs to be indexed)
    you can name the steps whatever you want, in some cases you will want to provide them with proper 
     names perhaps, because some steps can be reused throughout action 
    when you create an action that you can replay across many other actions, you will probably want 
     to set it in: runescape_commons
    the common_action_framework/ dir is for code that can be reused across other applications 
    the reusable_actions/ dir is for actions that can be reused across other applications
     you will probably not use them either of these much
    when running the tests: if you don't set the "extra_test_info" field
     the "verify" field is tested against the next step's test field, therefore, in your final step you can add a "test" field if you 
      want to test for that final "verify" field, otherwise, if you add a "extra_test_info" you will test the "verify" field 
       in the current step against the images in: "end_mock_image_list" 
       example:
        "extra_test_info": {
            "end_mock_image_list": [
                get_test_picture_by_name("test_existing_user"),
                get_test_picture_by_name("rs_app_requires_update"),
            ],
        },
    remember to change the 'id' of your final step
     



