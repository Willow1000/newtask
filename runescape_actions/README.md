#runescape_actions
# please ignore the formatting in this documentation on github, after you pull the branch, read it in your local editor

*this repo is meant to work alongside another repo: LocallyAvailableActionTooling, you must have access to that repo, without access you can only test locally
** creating a developer environment docs at: restricted_user_scripts/README.md (this is not for developers, it's for me)

section I:
1. docs index
 section I:
  1. will provide an overview of the basic elements, you should use the basic'este action here as an example, 
   that would be rs_login, it will also explain a bit of the scheduler (what you will be using to change 
    the state of what is running in real time), this is great to know, cause it will be your debugger
   1.2. overview of everything and where to start
  2. overview of how the bot is meant to do things
  3. framework documentation (basic concepts and basic elements, ofc the full docs for this are in: reusable_actions/README.md)
   3.1 what is an action
   3.2 basic elements of your steps (overview) 
  4. detailed step elements
   1.3 all_failure_elements dictionary explained
   1.4 explaining all the elements in an action  (IMPORTANT: you kind of have to know all of these)
   1.5 explaining all elements in a step
    1.5.2 multiple action possibilities 
     (example: how to add multiple possibilities to resolve the 'check' element(press something on screen))
     1.5.2.2 multiple action possibilities and get_action_picture_by_name using 0common_photos images
    1.5.3 test information (adding testing information to step)
    1.5.4 final step in every action 
    1.6 common step structure patterns (these are very important patterns you need to learn because they reappear often)
     *this part of the documentation will update often as more patterns start being more commonly used
     1.6.1 awaiting for an expected UI change to make a decision
  5. overview of local testing
  6. overview of how the action directory structure works
 section II: 
  1. how to build actions, what does each file do, etc.
   1.1 separating an action into "reusable" actions (auxiliary actions) 
   1.2 best way to separate actions or to create these auxiliary actions is to follow a simple pattern 
   1.3 folder structure of a specific action
    1.3.2 quick guide on how to take screenshots: 
   1.4 initial steps when creating an action 
  2. adding custom code into your actions, whenever the basic image matching isnt working out
   2.1 for documentation on what the step fields are: reusable_actions/README.md
   2.2 creating 'custom' steps
   2.3 accessing the bot state (README_bot_status_api.md) 
   2.3.2 profile and accessing the profile
   2.3.3 accessing running bot status (main functionality you will want to know)
   2.3.4 StepManipulator and step id naming
  3. testing your actions locally
   3.1 how to correctly test: which steps do I really need to test? 
   3.1.2 the test fields
   3.2 action_tests.py and testing infrastructure explained
   3.2.1 explaining local testing
   3.3 running Local tests
   3.4 analysing the output of local testing:
   3.5 correctly setting precision for a step as you are testing
  4. live testing your actions on a running system
  5. putting actions together (the scheduler) 
   *how the scheduler works and what you can do with it  
    (the scheduler is what you use to send the live running bot some commands)
 section III:
  1. development phases
  2. submitting a task for review


1.2 overview of everything and where to start: 
 the following gives you some instructions and steps on how/where to start, and some info on usually asked questions of what to do next?
 *this section (1.2) is meant to guide you through the rest of the docs to a point where you can get started 
  doing your own action (you will need more than a guide on where to get started to finish the action though)
 clone the repos
 follow the docs in: runescape_actions/readme.md
 *the docs will also lead to videos explaining most sections
 *make sure you keep an eye in the: #announcements_engineers channel, whenever there is an update, pull from testing branch and merge into your local branch
  also you want to enable notifications on: frequently-asked-questions and information-engineers
  and disable notifications on your -dev-channel, example thomas-dev-channel (that will be your id)

 as you are analysing the docs/videos
 you can try and analyse the actions that seem the most developed, which are: rs_login, cooking_raw_swordfish, in_game_pause

 first thing you want to be able to do is: local test
 try doing your local test with: rs_login like in the video, and 
  afterwards cooking_raw_swordfish action, analyse the output a bit as you watch the corresponding video, 
   make sure you understand everything and ask wahtever questions, this will be your first thing you will 
    do in your own action you will be creating

 after that you want to try and start your action, let me know and I will provide you with your first task

 you need to be able to access your in game account I send you, and you need be able to access it through my system.
 this is what I call the live test, which is how you run the bot.
 this is section II.4 of the docs, you need to be able to connect to my vpn, and be able to receive back the screen in your machine.
 Afterwards, you will be synchronizing your files with my remote server and  you will be able to run the bot.
 This is required before you start your action, because you will be needing to take a few screenshots ingame, for that you need an account, for that you need to one of my accounts, and for that you need to be able to connect to my system this way.

 after the above you are now able to start developing your action, take whatever screenshots you may require, and as you are creating your action, you are also able to local test
 When you are closer to the finish line you will also be remote testing it live, by this point will 
  also have wanted to watch the remote testing videos and using the scheduler example

 remember after you are given your task the first phase is to make the bot do that task, whatever you require doing, there are several phases, each phase I will probably give you an idea of what to do, they all pay different and some will be harder than others
  

2. overview of how the bot is meant to do things
videos explaining how some of the ingame tools will be used:
in the link: https://drive.google.com/drive/folders/1qmEy9bX8S6nEqld2EVsoTp5gR-qb6iIp?usp=sharing 
 there are a few videos, they were meant to teach people taking a few screenshots and developing the idea of the task, however, 
  they are also good to quickly understand some of the ingame tools you need to complete your tasks.
understanding the game and the ingame tools is essentially to be able to achieve your tasks
 
videos introducing you to the tasks, by explaining and refering to this documentation
in the link: https://drive.google.com/drive/folders/1RVQaL-BnBDv8EjZ8WIyBhVkAxTLwQHn9?usp=sharing 
 you will see a few videos explaining how to develop, but you need to understand the ingame tools and how to use them, because the bot 
  will need to use them, these videos will refer to this documentation and these sections
link to videos with the tasks:
 *you will have your task and I will send those tasks to this link if I have anything on them, you just 
  have to go into this folder and look for the task after we agree on your next task
 https://drive.google.com/drive/folders/1a0Vj0o56GF4nO-AQ8QaCKqa0mVxSCLOG?usp=drive_link 
   
3. framework documentation:
first a conceptual explanation with some examples:
 3.1.what is an action:
  so every action is just a bunch of steps:
   what is a step: it's just a json dictionary that specifies what the bot will do when it reaches that step
    to finish a step, you must resolve its 'verify' or 'jump' fields, so when you enter a step, the first it's looked at is the 
     'verify' field, if it's true, the 'check' field will not even be looked at, so you have to be careful when using these,
      so, if the 'verify' field fails you will enter the 'check' field, resolve it, and then continuously stay on this loop: 
       'verify' -> 'check' -> 'verify' until 'verify' returns True
  *to have a picture of the above, you can take a look at the rs_login action in runescape_actions/rs_login step 0
  returning True in case it's a function, BUT if it's not a function and it's the name of an image (most common)
   this the program is going to look if the image exists on screen (the image is the png with the name the string in the field),
    this is case for 'check' and 'verify' fields, AND if the image exists on screen 'verify' field will be similar as returning 
     True and the next step will be reached, in the 'check' field case, if the image exists, it will press it in some fashion
  check step 7 in rs_login for an example on using functions as well

 3.2 basic elements of your steps (overview):
  *for more basic elements info: this is just an index, we will go through all of this in more detail below:
    reusable_actions/README.md
  to understand where the photos come from, check: get_action_picture_by_name, the examples are quite simple 
   if you check rs_login action you can see the base path where you are getting the photos from is: 
    "action_name"/all_action_files/screenshots/ in the action folder
   however, you can also grab them from runescape_actions/commons/0common_photots/ which will be photos common to 
    all actions in runescape for example, this is a bit more explained in 
  more fields associated with the 'verify' field: the "reverse_verification", (in case you want to verify if something doesnt exit), 
   instead of something existing, "verify_mode":
    *verify_once*: verification step is true if at least
     one of the images in the 'verify' field list
      is found
    *verify_all*: requires all images to be found, default is verify_all, optional field
    default is verify_all
  next would be the 'jump' field, example:
   "jump": {
       # a conditional jump, an if-else condition, in this case, representing a while loop between the current step and "step_num"
       # (it jumps if the condition in verify is false)
       "step_num": "change_world",  # here step can be a number or an id, however, an id will always be the correct id,
        # even if you later on add a step in between, also if you add a step id here, remember it jumps to the 
         # first step id that STARTS with "change_world", so ALWAYS make sure your step ids are completely unique and 
          # not very similar at all, even if convenient
       "verify": get_world_verification_for_current_account,
       "verify_mode": "verify_once",
       # verify_mode verify_once means that you only need to verify one of the images from the
       #  'verify' field list
       "reverse_verification": False,
       # "reverse_verification" reverses the condition required to verify the image (BEWARE: this will work together with verify_mode)
       #   it's the same as saying 'not verify get_world_verification_for_current_account'
   },
   this means: it will jump to step 6 if the function in "verify" field resolves to FALSE(a particularity of the "jump" field)
  for more basic elements info: this is just an index, we will go through all of this in more detail below:
    reusable_actions/README.md 
  
 4. detailed step elements
   ( following numbering according to the file: reusable_actions/README.md  ) 
    1.3 all_failure_elements dictionary explained
    1.4 explaining all the elements in an action  (IMPORTANT: you kind of have to know all of these)
    1.5 explaining all elements in a step
     1.5.2 multiple action possibilities 
      (example: how to add multiple possibilities to resolve the 'check' element(press something on screen))
      1.5.2.2 multiple action possibilities and get_action_picture_by_name using 0common_photos images
     1.5.3 test information (adding testing information to step)
     1.5.4 final step in every action 
     1.6 common step structure patterns (these are very important patterns you need to learn because they reappear often)
      *this part of the documentation will update often as more patterns start being more commonly used
      1.6.1 awaiting for an expected UI change to make a decision
      1.6.2 reusing an action in another action
  
 5. overview of local testing
  *for more and more detailed information on local testing: section II: 3.1, 3.2, 3.3, 3.4
  here we have an overview:
   it's simple to refer to the video to explain the output of the test and how the "test" fields work
   to understand how the test files work, we must go to section II, 3.1,...
  overview of action_tests.py 
  comparing the action_tests.py file of an action with dependencies, with action without any dependencies:
   rs_login action (no dependencies) to cooking_raw_swordfish action (with dependencies)
  *depencies just means, an action that uses parts of another action, or another reusable action, due to limitations 
   the code for the test must take this into account, this will make more sense once you understand how to reuse an action 
    a bit better (section II.1.1)
 
 6. overview of how the action directory structure works
  to run the local tests, check: ( 3.3 running Local tests ) 
   action_logic/ contains all special logic for an action, any code you need to make that is specific to the action, 
    you can add it here
   all_action_files/screenshots/action all the action images this action requires
   all_action_files/screenshots/test all fullscreen photos to test the above action images in
   action_explained.txt, this file explains the steps and how your idea went on structuring the steps
   action_tests.py: see ( section III.3.2 ) testing and action_tests.py  
   test_expected_output_explained.txt: see section 3 as well
  how to start:
   (see section II. 1.4 ) for a detailed overview
    
 
section II:
building actions: 
 1. action folder structure
 
 1.1 separating an action into "reusable" actions (auxiliary actions), I just call them "reusable"/"sub actions", 
  *this can be a second phase of your development, to properly divide things, however, you need to start 
   things with an idea of what to expect
  if you look at the runescape_actions/runescape_actions folder 
   you can see there is a commons folder, in that folder everything (besides the jobs/ folder we already talked about)
    is an auxiliary action, which is an action that will be by other actions (it's like a function you can reuse)
  example: if you analyse the cooking_raw_* actions, you can see they all use the commons/cook_fish action, they import this action 
   and change a few things, how do you change these things?, you can follow the pattern in the file commons/cook_fish:
    the main thing is the function update_action, which will:
     Update multiple steps in the action's ordered steps based on a list of updates
      each element in the updates list is also a step dictionary, identified by the "id" key, everything in this step will 
       override or be merged into the original step with the same id in the action_ordered_steps list
  example:
   create a function that updates the dictionary:
    def get_cook_fish(updates=None):
        if updates is not None:
            ordered_steps = copy.deepcopy(action_ordered_steps)  # copy or you will be changing the original
            updated_steps = update_action(ordered_steps, updates)  # update_action applies every update in updates(by step id)
            return updated_steps
        return copy.deepcopy(action_ordered_steps)  # always return a copy of the actions(python passes by reference so you have to send a copy or you will be changing the original)
    and import this function wherever you need it, in this example that would be all of the cooking_raw_* actions, each of 
     them with different lists as the updates argument of the get_cook_fish function
   the update_action function being the most important function here:
    it receives the updates list in cooking_raw_swordfish/action_description.py and applies the update to every element with the id 
     of the element of the list, it changes everything you provide to the step with that id
   *this is also a common pattern that you can see in: reusable_actions/README 1.6.2
   
    
  1.2 best way to separate actions or to create these auxiliary actions is to follow a simple pattern:
   obviously it depends from situation to situation, but usually separating with the following objectives in mind:
    1. action setup phase 
     example: buy all requirements and deposit to bank, and move to the required location that you need to cook fish
    2. repeatable phase
     2.1 setup requirements for the creation method
      example: withdraw requirements from bank (withdraw auxiliary action already created, you must import and use it)
     2.2 loop creation method
      example: cook a fish X times
     2.3 cleanup to be able to set the state back to the start of 2.1
      example: deposit back the output (deposit auxiliary action already created)
    3. action cleanup phase 
     example: you will need to go back to a neutral region where the bot can go to its next action, basically you must 
      take the bot to a state such that it is equivalent to the state it was before the setup phase

    in the above example, you would need to create 3 actions and each of these actions would have a variable number of 
     arguments, for amount of required materials to buy in action setup phase, how many repeateable iterations in repeatable phase,
      these are a rule of thumb, obviously it will depend from thing to thing
    in general separating these 3 phases is ideal, this way I can do the action setup phase for a few different actions in a row, 
     and then decide what to create first, and then I can have a single cleanup phase, depending on the situation
    you have to imagine your task in the following way:
     example: you have a cooking action, cook pizza. and your task is to subdivide it: lets subdivide it:
      1. buy all requirements to cook 100000 pizzas, deposit them in bank
       *abstract deposit to the bank(already done at this stage of the project) 
       *same for buying stuff
       may require moving to some specific spot (movement is very specific and will need to be done at a later stage)
      2. cook 100000 pizzas
       2.1 action that checks if everything is ready to start and withdraws from the bank, the requirements for 10 pizzas 
        (we will be cooking 10 pizzas at a time)
        * abstract withdrawing from the bank(already done at this stage of the project)
        checking if everything is ready is very action specific, example: 
         you can look at the inventory and see if everything that is there is supposed to be there
        may require moving to some specific spot (movement is very specific and will need to be done at a later stage) 
       2.2 subdivide into cooking (you can abstract cooking pizza into cooking, such that you can use the cooking action 
        in the cooking pizza action and the cooking in any other cooking action, like cooking salmon, well if you abstracted a
         cooking action correctly, you can now use it in the cooking pizza and the cooking salmon actions that you will do later!)
       2.3 deposit the 10 pizzas to bank
        *abstract the deposit (such that you can use deposit pizza, salmon, logs, wood, gold (this is already done at this stage))
       **repeats to start of 2.
      3. sell 100000 pizzas
     *it seems harder than it is, the method above actually allows us to create several actions at once, we are essentially 
      ideally we would be creating the actions for cooking pizza and salmon almoust simultaneously (this is just an example), 
       but it is common to happen that two actions are super similar

 1.3 folder structure of a specific action
  ( already explained in section I.6, this was left here for reference )
 
 1.3.2 quick guide on how to take screenshots:
  *** you can use the scraper tool, to scrape the images of the internet, this is super useful for 
   item images, not so much if you want to get object images, in this case and with a lot of items (that fit in your inventory), 
    you will not need to take any screenshots (usually), however, if you do, u will need to login to do it, or try and take your 
     images from the videos
   this tool is in: LocallyAvailableActionTooling/scraper.py
    it's simple to use, more info in: LocallyAvailableActionTooling/README.md section 3.
   you must see the other things you need to have attention to when taking screenshots in:
    LocallyAvailableActionTooling/README.md  (sectio: HOW TO TAKE SCREENSHOTS) 
    *make sure you have 100% zoom and 100% brightness, otherwise you WILL have trouble with the screenshots 

 1.4 initial steps when creating an action
  1. just start by copy pasting the rs_login action and rename the action_id in the action_description file
   first thing to do is: to change the directory name of the rs_login action to something else,
    when doing this make sure you also set the new action id in the action_description: 
     the name of the variable is: current_action_id, you must set it to the same name as the chosen 
      action id name for your directory, you will need to set this new action id in most of the testing tools
  2. delete the previous pictures from the all_action_files_screenshots/action and test folders as
   well as the previous action_explained.txt
  3. create a new file: action_explained.txt in that action's directory, where you explain
   what each step is going to do (HOW? read below: HOW TO CREATE THE action_explained.txt file)
  *after you created your action description, or as you are testing certain steps:
  4. afterwards delete all the steps from action_description.py, dont forget to change the action id
  5. you can change the main things in action_tests.py: the class name, the hooks, the imports in run, 
    and you will have more details on how to build this file in 3.2, however, you will always be building it 
    the same way, you can see examples in: rs_login and cooking_raw_swordfish actions
  6. after running the local tests: explain anything that's hard to understand in the file: 
    test_expected_output_explained.txt 
    hard to understand means: you understand it, however it's somewhat unexpected, 
     but the reader of the output of the test may have some trouble understanding, 
      so for quick understanding write it down and explain it
  7. remember that before pushing the code to the repo: format the code with ruff, 
   using the settings in the ruff/ruff.toml file
  
 1.4.2 HOW TO CREATE THE action_explained.txt file:
  (you have to do it in a specific way to make sure it's easily parseable)
  *check rs_login action example:
  1. first line is action id: 'action_id'
  2. second line is app_id: 'app' (example: runescape)
  3. the optional line starting with: new_plugin_list: 'plugin1,plugin2', this is only for plugins
   you added on top of the basic plugins already set below (search for: basic plugin list), it's important you dont forget this one
  4. all the lines starting with the descriptions of what you are trying to do, example:
   1. TODO: it's selecting the flower at the top right of the screen, out of all the seven flowers
   2. select shovel
   3. select ...
   this way, whoever is fixing this can have more detailed information, a line shouldnt have a TODO
    with no more information
  but overall, and ideally the steps should just be descriptive, and remember to update them before you push as well, 
   this is because once you are done with the action, the initial idea probably does not match the final solution

 1.4.3 action fields:
  *these are fields specific for the whole action, they are variables within the action itself
   example: in_game_pause action has all these fields there
    time_limit = None  # time limit for this action (in minutes) (this is usually None)
    current_action_id = "in_game_pause"
    app_config_id = "initial-config"  # each action may require a different set of configs from the app itself
     # the default that you should always use is: "initial-config" I will change this later if I must
    context = "rs_ps"  # context to know what profile to use, what is this session related to, etc.
     # you dont really want to change this, it should always be rs_ps
    settings = {
        "reloaded": False, # "reloaded" field means: every time we use this action we will reload it 
         # this reloaded may be useful if the action has variables that we need to change at the start of the action, 
          # everything that needs to change at the start of the action will change if set reloaded to True 
           # this will usually be False, and the default is False
    }
    # settings are the settings for the action, this may change and if it changes further documentation will be added  
   ** you will usually leave it as it is above, the only thing you will change is: current_action_id, everything else 
    is quite specific and we will be talking if you need to change it
  
 2. developing using the framework
  this section is about developing your actions, and extra tools you can use to access internal states
 2.1 for documentation on what the step fields are reusable_actions/README.md:
   ( this is the same as section I.1.4 )
  
 after understanding how to build steps properly, we can move on

 2.2 creating 'custom' steps
  *custom functionality for your steps, (this will be updated constantly as the project advances, it will require more and 
   more functionality, that will most likely be shared by all)
  the basic functionality from 1. allows to create some interesting things, however, we are still missing custom functionality we  
   want to add in, to do this it is allowed to use custom functions in the 'check' and 'verify' fields, as mentioned above
  full information about building custom steps in file: README_bot_status_api.md
 (from: README_bot_status_api.md) 
 2.3 accessing the bot state
 2.3.2 profile and accessing the profile
 2.3.3 accessing running bot status (main functionality you will want to know)

 3. testing your actions locally
  3.1 how to correctly test: which steps do I really need to test?
   not every step requires a 'test' field, it's really just common sense and experience that will show you what you need 
    to test, but the same way you dont really test everything when you are coding, there is no need to test everything here, 
     for your first action, you will be testing everything
   as a general rule of thumb:
    add a "test" field to anything that uses *_click_highlighted
    no need to add anything whenever you use a photo you find with the scraper***(explained below)
    any photo you add to action/ manually it's just better to test it's just faster overall
    "jump" fields are great to test
    in case you use any photo that already exists in: commons/0common_photos/*, and is an image you just added
     there is no need to test
   ***scraper: this is a tool you can find in LocallyAvailableActionTooling/scraper.py
    when you execute it you will see you have to choose the action id, this is for the scraper to add the 
     scraped image directly into action_directory/all_action_files/screenshots/action/*
    for more information: LocallyAvailableActionTooling/Readme.md section 3.
     
  3.1.2 the test fields
   *we can take as examples, cooking raw swordfish action and rs_login action, remember that:
    the cooking raw swordfish action as "sub" actions it uses, namely: cook_fish, deposit_bank 
    
   "test" field: 
    example:
     "test": [
         {
             "mock_image": get_test_picture_by_name("terms_of_service_test_screen"),  # the image the "check" field will test against
             "replay_input": {"replay_type": "mouse", "coords": None},  # replay_type is either: mouse or keyboard, the coords can 
              # just the coords you are expecting to be pressed OR, None (will be testing 3 times, hopefully the coords are close)
               # 99% of the times coords: None is the right choice, unless you are trying to do something special  
         },
     ],
   "extra_test_info": for while loops in general, we can take as an example: 
   example from step 10, rs_login:
    "extra_test_info": {
        # loop_info already handles 'end_mock_image' in a way
        # "end_mock_image_list": [ get_test_picture_by_name("password_inserted_screen") ],
        "loop_info": {
            "num_iterations": 1,
            "img_after_loop": get_test_picture_by_name("test_verify_world_308_pressed"),
        },
    },
     
    you can also use it to test the "verify" field of the current step, if it doesnt exist, the "verify" field will test 
     against the "test" image of the next step, so you kinda wanna use this in the last step if it's a complicated thing
      you are testing, or if the next step is a bit complicated, like a jump step or something, you usually dont want to 
       add a "test" field in a jump step
     example: 
       "extra_test_info": {
           "end_mock_image_list": [
               get_test_picture_by_name("test_existing_user"),
               get_test_picture_by_name("rs_app_requires_update"),
           ],
       },
       here instead of testing against the "test" image list of the next action, you have a more fine-grained control 
        that you are testing against a list of images of the current step
     
   *for documentation on all step fields, check: reusable_actions/README.md
     reusable_actions/README.md 1.5.3 test information 
   
    
  3.2 action_tests.py and testing infrastructure explained
   *we can take as examples, cooking raw swordfish action and rs_login action, remember that:
    the cooking raw swordfish action as "sub" actions it uses, namely: cook_fish, deposit_bank 
   this section is for local testing
   testing in your real environment is section II: 4.
   local testing is prior to testing in a real environment, altough you will be using both interchangeably, 
    however, local testing gives you the most power, cause you will not have access too your environment logs
    
   test_expected_output_explained.txt, this file explains the local test output of each step
    the required sections are: 
     TODO: anything you feel is missing (can be empty)
     EXPECTED OUTPUT: (expected output of the local testing stage)
      this is for steps that you feel like need special explaining when looking at the local test results
       this will be the first thing I look at if something unexpected is happening in the local test results, 
        it is expected you have the common sense on how to write this properly after a while
   in rs_login action we have an example of this file:
    *that is just an example of what you can explain, the only REAL thing that you really need to explain in rs_login expected output 
     file is the step id: "loop_until_world_selected", cause it explains the decision to increase base precision there
   
  3.2.1 explaining local testing
   the action_tests.py file of the cooking raw swordfish action is the one we will be looking at 
    to explain the local testing 
   class CookingRawSwordfish(Test) 
    u always need to extend the Test class, the class name is always the same as the action
    
   always need to change the run function: 
    in the following action(cooking raw swordfish) you have:
    def run(self):
        print('testing cooking raw swordfish') # remember to change the print message
        from highalching_combat_bracelet_at_fountain_of_rune.action_description import time_limit, current_action_id, \
            app_config_id, context 
        self.full_test(None)  # this will call the main_test function and write the report, None argument, cause 
         # we are overwritting full_test and building it from scratch
     
    in the rs_login action, you have:
      def run(self):
          print("testing rs login")
          from rs_login.action_description import time_limit, current_action_id, \
              app_config_id, context 
          from rs_login.action_description import action_ordered_steps
          self.full_test(action_ordered_steps)
     
    the full_test seems like different functionality in both, 
     full_test will just call main_test at one point, which default implementation just tests the provided 
      action_ordered_steps, therefore, what you can do is: either build the correct action_ordered_steps 
       in run method, OR just overwrite main_test functionality, it's kind of the same thing, so I will just 
        go with overwritting main_test
     
   overwritting the main_test function:
    main_test(self, action_ordered_steps_current_action)
     in this example:
      we just have:
       def main_test(self, action_ordered_steps_current_action):
           from cooking_raw_swordfish.action_description import cook_raw_swordfish
           from runescape_actions.commons.cook_fish.action_tests import CookFishTest
           from cooking_raw_swordfish.action_description import deposit_cooked_swordfish
           from runescape_actions.commons.deposit_bank.action_tests import DepositBankTest
               
           # the reusable actions (or different actions used inside this action)
           self.incorporate_test(CookFishTest, cook_raw_swordfish)
           self.incorporate_test(DepositBankTest, deposit_cooked_swordfish)
            
           incorporate_test just uses the main_test functionality of a previously created test, 
            this is so you can reuse tests of actions inside other actions, that's why overwritting 
             main_test is always a better idea
       
      using incorporate_test has the main_purpose of using another class's hooks_setup and any other specific 
       changes we added into the main_test functionality 
      
      hooks_setup method overwritting, you must always overwrite this one as well 
       in the following example:
       class CookFishTest(Test):
           def hooks_setup(self):
               hooks = {
                   'click_fire': { 
                       "check": self.hook_highlight_step,
                   }, 
               }
               self.set_hooks(hooks)

       the hooks_setup overwrites the step with id: click_fire and sets its "check" field to self.hook_highlight_step 
        hooks_setup in rs_login overwrites a bunch of stuff with: none_step_verify_hook, which just means 
         we dont care to test whatever is there, and it has to be quickly explained in: 
          test_expected_output_explained.txt file why that is
         and we also created specific functionality to test a few steps: self.get_test_world_string_test
          which is created in the test class itself
       
      all existing premade methods are:
       hook_highlight_step, used whenever you have to a region within the borders of an highlight
        example: any time you click_highlight stuff you will want to overwrite it with the self.hook_highlight_step premade method 
       hook_template_matching, used whenever you want to hook a template match function
       none_step_verify_hook, used when you want to ignore any function or want to hook a none_step_verify, uses:
        ignore_function, very useful, because it ignores the function, but still prints output information


  3.3 running Local tests
   run a single test command example:
    you must first set the environment variables: 
     export CLIENT_MANAGER_PROJECTS_PATH="path of the directory containing the runescape_actions repo and the LocallyAvailableActionTooling repo"
     export PATH_CONTAINING_COMMON_ACTION_FRAMEWORK="path of the directory containing the runescape_actions repo and the LocallyAvailableActionTooling repo"/runescape_actions/common_action_framework
     and set them in your .bashrc (that's how you set environment variables in linux)
     *it's better if you just have runescape_actions repo and the LocallyAvailableActionTooling repo in the same directory 
    cd "path_containing_your_runescape_actions_repo_path"; "venv_path"/python ./runescape_actions/runescape_actions/rs_login/action_tests.py --current_action_list_projects_path="runescape_actions/" run
     you can also add:  --minimum_image_precision="0.8" argument as explained in ( section I.6 video), the default  --minimum_image_precision is 0.6
     "venv_path"/python: is your created venv path's python executable, 
      you probably created it following instructions from LocallyAvailableActionTooling/README.md 
     "runescape_actions_repo": self explanatory
     "path_containing_your_runescape_actions_repo_path" is the path the contains the directory with your runescape_actions repo
   an example of running this command for action: cooking_raw_swordfish
    cd "path_containing_your_runescape_actions_repo_path";
    python .\runescape_actions\runescape_actions\cooking_raw_swordfish\action_tests.py --current_action_list_projects_path="runescape_actions/" run
       

  3.4 analysing the output of local testing:
   when in a composite action (an action composed from many other actions), the output is a bit more complex, the output usually 
    goes into: "runescape_actions_repo_path"/local_test_output
     and we will be focusing on the following action's test output: local_test_output/cooking_raw_swordfish, which is a bit complex
    there will be a couple folders here: 
     dependencies folder, which will contain the local test output for each of the reusable actions that compose this action you are 
      testing
     unique_images_for_this_test folder, which will contain all the unique images that were obtained specifically on this test,
      what happens a lot is: the images are tested on images that we tested the reusable actions this action contains within it, 
       and the images being tested are not real images, they are just a reminder of the previous test 
        in this folder, we try to make sure that all the images that appear in the folder are images specific to this test, such 
         that you have quick access to everything unique that you are testing in this current action
      outside both of these folders you have the whole test, all the acquired images while testing 
      you also have a test file: full_report_cooking_raw_swordfish which is the full report of this test, this is basically 
       what is outputted on your command line, the parts I deemed most important, at least
     I suggest you open all the images in a photo viewer that has a slideshow and just slide throught them to check the output
     once the output is what you expect, just move on to live testing
  
  3.5 correctly setting precision for a step as you are testing
   as seen in the video, when testing the default precision should be 0.6, testing itself is a method to visualize better 
    what precision may be required for a specific step in an action, to change this precision, we already know a bit of how it works: 
     in rs_login action, step id: "loop_until_world_selected" we have an example, to have an idea about the precision we must 
      analyse the output of the test, which you can find in the test output folder's directory: a file named: full_report_rs_login 
       or you can just see the output of running the test in the terminal (as explained in 3.3 )
   after having analysed the output and understanding the precision requirements as explained in the video, you must 
    set the precision just like in the example in: "loop_until_world_selected" step, notice that the name of the field is different 
     when setting the precision for the "verify" and "check" elements
  
  4. live testing your actions on a running system:
  TO START RUNNING YOUR ACCOUNT AND GET THE SCREEN OF THE APPLICATION BACK TO YOU:
   take a look at ( LocallyAvailableActionTooling/README.md 4. ), it explains quite well what you need to do and all the requirements
   make sure you only run these tests after you are satisfied with your local tests
    these tests will not really have any output logs that you can see, and you wont be able to get much feedback other than 
     what you can see that is happening on screen
   you will also need the X server software: VcXsrv (on windows)

  5. putting actions together (the scheduler):
    so a bunch of bundled actions I call a session
    grouping sessions and their configurations are set in a scheduler update file
     you can find these template_scheduler_updates in: LocallyAvailableActionTooling/template_scheduler_updates
    example:
     { 
         "jobs": {
             "target_accounts": ["bot2", "bot3"],
             "target_client_of_class_id": "rs", # this is the server id, no need to touch this for now
             "app_config_id": "buy_sell_config", # this is the game configuration
             "job_order": ["rs_login_job", "trade_at_exchange"], # ordering of the jobs below, must have the same ids
             "sessions_metadata": {  
                 "update_type": "reload"
                 # update_type is:
                 #"reload" will reload the entire job configuration (creates a new running bot status), and info 
                 #  will be lost on the previous running bot status, which can be just fine
                 #"update" will update the current running bot status, and info will be kept on the previous running bot status,
                 #  any new added sessions will be appended to after the current sessions, and run after them
             },
             "jobs_to_run": {
                 # jobs are actually defined in: runescape_actions/jobs
                 # "rs_login_job" here is the "id" field of the corresponding job in runescape_actions/job
                 "rs_login_job": {
                     "sessions": {
                         #this is an example, I go into the "rs_login_session" and I overwrite the "config_required_in_app" field,
                          #this would overwrite the field, but will also add it, if it doesnt exist
                         "rs_login_session": {
                             "config_required_in_app": "buy_sell_config"
                         }
                     }
                 },
                 #same for this one
                 "trade_at_exchange": {
                     "sessions": {
                         "trade_at_exchange": {
                             "config_required_in_app": "buy_sell_config"
                         } 
                     }
                 } 
                 #there were 2 jobs here, they will be executed sequentially by each client in target clients
             }
         }
     }
     you can learn more about these fields in: LocallyAvailableActionTooling/template_scheduler_updates/README.txt
   
    in the above example u are setting the next jobs
    you can also set the state of the running job and actions by manually setting their state
    we can explore the example of setting a simple state file:
    LocallyAvailableActionTooling/template_scheduler_updates/control_flow_manipulation/manipulating_running_bot_status.json
    example:
        "jobs": {
            "target_accounts": ["all"],
            "target_client_of_class_id": "rs",
            "sessions_metadata": {
                "update_type": "update",  # explained in example above
                "is_looping_in_current_session": false,  # if it is looping in only this session and not going to next session (so u can debug)
                "changes_to_current_running_action_status": {
                    "step_num": 4,  # sets the current step to this step
                    "temporary_session": "none", # removes any temporary sessions (see below)
                    "current_running_state": "running",  # "stopped" or "running"
                     #"current_running_state": this is how we stop/resume the service, the options are:
                      #"running", "stopped", "NA"(nothing changes)
                       #default value is "NA"
                    "running_action": "none", # "none" is no change, but you can give it an action id within the session
                    "running_session": "none"  # "none" is no change, but you can give it a session id, the session ids are as below
                },
                "sessions": {
                    # helps debugging a specific session, or action
                    "rs_login_session": [
                        { 
                          # this defines where the running session will start, where it will end, what action it starts in
                          "action_name": "rs_login",  # helps debugging a specific action
                          "starting_step": -1,
                          "final_step": -1,
                          "is_looping_in_action": false,  # if it is always looping in the current action and doesnt go to next action 
                          "is_skipping_to_next_action": true # if it is allowed to skip to next action or not
                          # if: "is_skipping_to_next_action": false AND "is_looping_in_action": false, it will be stopped after finishing action, which can help a bunch debugging
                        }
                    ]
                }
            }
        }
    in the next example, we will look at what a temporary session is: 
     well, it's just a temporary session that will revert to its previous state (previous session) once the temporary session ends, 
      it will revert everything, the need to create this arised from the need to do something manually without disrupting the natural 
       state of whatever is already running, for example to pause in game, example json:
        in game pause, from control_flow_manipulation/in_game_temporary_session_pause.json 
         "jobs": {
             "target_accounts": ["all"],
             "target_client_of_class_id": "rs",
             "app_config_id": "in_game_pause",
             "job_order": ["in_game_pause"],  # in_game_pause
             "sessions_metadata": {
                 "update_type": "update",
                 "is_looping_in_current_session": true,  # says that the temporary session loops, meaning it will 
                  # run forever until you manually stop/revert the temporary session, to revert just set the type under 
                   #"temporary_session" field
                 "changes_to_current_running_action_status": {
                     "step_num": 0,  # everything  you set inside here is in respect to the temporary session
                     "temporary_session": {  # tells it's a temporary session
                        "job_id": "in_game_pause_job",  # says what job will be running
                        "type": "toggle" # toggle means toggle, next time u send this exact same json it will revert the temp session
                     },
                     "current_running_state": "running",
                     "running_action": "none",
                     "running_session": "none"
                 }
             }
         }
      *notice that this is completely different than the pause_running_bot_status.json, this is because this pauses 
       inside the game, which doesnt mean the steps stop processing at all, some games require you to do something 
        while the character is waiting inside the game, otherwise, you will automatically log off, this is what 
         in_game_temporary_session_pause.json corresponds to.
         The pause_running_bot_status.json on the other hand will stop processing steps for the target account 
          at the current step, whatever it is doing
         you also have the resume processing json: resume_running_bot_status.json, these are all just quick to use things, such 
          that you dont have to do it from scratch every time
      5.1 reloading an action:
       in some cases you can reload an action without restarting your system from scratch, you can just hotload it in, example:
        your action has a bug you quickly fix and want to retry it again:
         from the json: control_flow_manipulation/reload_action.json, example:
           {
              "server_side_options": {
                "reload": [ # just set the list of actions to reload in this field
                  "trade_at_exchange",
                  "rs_login"
                ]
              }
          }
       and it will reload all the actions, after you upload them to the server ofc,
        as to date, if you change anything other than in the runescape_actions/ folder inside the repo folder 
         you will have to restart your system, this reload only works on actions's code
       you will probably want to pause the bot and maybe set its current step before you reload an action
          
      5.2 testing after creating a new action:
       5.2.1
       you need to:
        1. create the job in runescape_actions/jobs
        2. create your scheduling file: job_scheduling/"subject"/ or use the jobs editor to output it directly into the correct place
         I suggest following the example in: schedule_login_and_await_with_in_game_pause.json file
          this way, you can automate login to the game AND test your action right away in a second screen or in the background
           OR you can just use the schedule_login_and_await_with_in_game_pause.json which and then only create the file to schedule 
            the action itself, this is probably the best way to do this
         the jobs editor is in: LocallyAvailableActionTooling/schedule_jobs_editor.py
        3. the output job should be copied into a specific place, and then use rsync to send it to the special 
         job location remotely:
       5.2.2 HOW DO YOU SEND your scheduler updates to the server:
          section 4.5 in LocallyAvailableActionTooling/Readme.md to have an idea of the file paths you need to set up
          you have to send your scheduler file to a special place in your remote file server


section III:
1. development phases:
 1. initial phase will focus on getting your task to work, the bot gets to the purposed end goal
  1.1 local testing (section II 3.)
  1.2 once local testing is passing every expected output, proceed to test it in your remote environment
  1.3 set possible TODO steps in action description in case there is something that cant be done now, but will be done 
   in the future
 2. second phase: dividing your actions (section II 1.2), you will also be creating a setup and cleanup task here
  as you are subdividing your tasks you will also be seeing where/what you can reuse for actions that are basically the same, 
   but with very small changes
 3. third phase: all task variations (all variations of the task, ex. craft gold bracelets and craft gold ring are 
  almoust the same thing, just a tiny change and that variation is set)
 4. fourth phase: multiple action possibilities (instead of just left click, you can also right click -> click option, 
  sometimes this is enough for multiple action possibilities)
 5. fifth phase: error handling, possible errors, explaining possible errors and problems in files, and error fallback
  final thing to do: implementing your task into a scheduler task

2. submitting a task for review 
  we will be constatly talking through the process probably, but ideally I need:
   a video of the bot running when you have 
    finished up, so just send me the video in discord of the bot performing your action on the live test, after I see it 
     I will review the code of your action, after it is reviewed you will be payed accordingly
  **due to the nature of the project it's possible some tasks have to be left unfinished for a while in case something is 
   missing to finish them up, in these cases we will have to subdivide the task and the payment must be reviewed, ideally 
    the person who started a task will later finish it and get the rest of the payment, because it will be faster for them



special considerations:
 the actions: 
  trade_at_exchange cannot be changed directly, it can only be used in other actions and changed in other actions, 
   if that action requires changes u will have to tell me
   


FAQ:
Q: I see the screen but it's all black and the game doesnt start properly, what to do?
A: send me a message right away, the problem is probably that the runelite app has updated, and I have to update it on my end, 
 this will happen sooner or later, and there really isnt a way to let you do this update in a simple way, therefore, this is a problem 
  that will be recurrent, I will try to fix this as soon as possible on my end. If the problem is different it may require more time ofc
Q: how should i connect reliably to the remote system? 
A: you should do this from within a VM/( prefirably for you docker container ) that you can share your text editor's files with,
 however, I dont provide a guide to any of this, you will have to figure it out, you can also choose to not use a VM, however, 
  it's always advisable that you use a VM when touching/interacting with an unknown system
Q: how much per task?
A: it will depend on the task, before you start the task we will talk about it, if the task ends up being a lot more effort on your end 
 we will figure out a better pricing for your next task.
 Remember that you always get paid for each task complete, and only when it is complete
Q: there will be a video on some of the actions, some actions are already halfway completed, what to do in these cases?
A: the purpose is to have the bot doing the whole task you need to bot, however, it may be that some tasks may be halfway through, but 
 they may be wrong, therefore, you may need to just recreate everything or simply just adjust it, the idea is that before you start 
  the task you have a couple hours to see everything about the task, understand it and then have a quick call with me with a proper 
   plan on how to implement it, specially when you are starting out

  
 
runescape app configurations:
 *this is mostly a reminder of every plugin that is being explored, in the base thing, 
  if you add any other plugins, remember to add that information in the action_explained.txt file for 
   that specific action
basic plugin list(the plugins present in all actions):
 Runelite mod settings:
 animation smoothing
 anti drag
 bank
 bank tags
 chat commands
 developer tools
 entity hider
 fps control
 fishing
 gpu
 grand exchange
 ground items
 ground markers
 idle notifier
 implings
 instance map
 interact highlight
 interface styles (2006)
 key remapping
 login screen
 low detail
 minimap
 npc indicators
 object markers
 player indicators
 quest list
 roof femoval
 run energy
 screen markers
 skill calculator
 spell book
 tile indicators
 world hopper
 world map
 xp drop

-runescape app considerations
 -you may define what plugins to use in
  settings.properties, however, the plugins
   in the plugins/ folder will always be installed,
    if they don't match or are outdated,
     you will receive a message in-game to update them




