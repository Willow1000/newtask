import os

if __name__ == "__main__":
    print('setting up new action directory in current directory')
    os.makedirs('temp/all_action_files/screenshots', exist_ok=True)
    os.makedirs('temp/all_action_files/screenshots/action', exist_ok=True)
    os.makedirs('temp/all_action_files/screenshots/test', exist_ok=True)

    with open("temp/action_description.txt", "w") as file:
        pass
    print('setup done')

    help_string = """
     HOW TO CREATE A NEW ACTION:
      an action is just a series of steps to perform the task at hand, whatever it may be
     make sure to add into the temp folder a video explaining what to do inside the game to 
      create the action, the video SHOULD be a short video, and should only show the steps needed to 
       perform the action

     after creating the video, make sure to create a file called action_explained.txt BASED on the 
      created video, that does the following:

     HOW TO CREATE THE action_explained.txt file:
      (you have to do it in a specific way to make sure it's easily parseable)
      1. first line is action id: 'action_id'
      2. second line is app_id: 'app' (example: runescape)
      3. the optional line starting with: new_plugin_list: 'plugin1,plugin2', this is only for plugins
       you added on top of the basic plugins already set below (search for: basic plugin list)
      4. all the lines starting with the step numbers, example:
       1. selects something
       2. selects something else
       3. ...
       each of the above step descriptions in its own line, if some of these steps are more complex,
        you should add a TODO on them at the start, but still explain what they are supposed to do, example
       1. TODO: it's selecting the flower at the top right of the screen, out of all the seven flowers
       2. select shovel
       3. select ...
       this way, whoever is fixing this can have more detailed information, a line shouldnt have a TODO
        with no more information
     """
    print(help_string)


