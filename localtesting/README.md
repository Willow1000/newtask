# LocallyAvailableActionTooling
dev tools to help develop the actions

requirements are as follows:
 clone this repo and the actions repo
 you will need to install:
discord
XLaunch (https://sourceforge.net/projects/vcxsrv/) or xorg if you are on linux (if you are on linux/mac you will have to figure this out yourself)
on Linux: 
python3: 
 (python version 3.10 minimum I believe)
 sudo apt install -y python3 python3-pip (I am not sure this will always install 3.10 minimum, you will have to see)
  you will have a better idea if it all works after you install the requirements in a virtual environment
xorg and xephyr: (instead of XLaunch for linux (I think it works, but you will have to figure this out yourself like I mentioned above))
 sudo apt-get install xorg -y
 sudo apt-get install xserver-xephyr -y
some other dependencies on linux that I know of:
 sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev python3-tk tk-dev python3-dev python-tk 
I advise using wsl for point 4. you can use whatever you wish, it's probably all going to be easier with windows and wsl

1. app setup
 for runelite (runescape): all_app_profiles/rs_profiles/* content must go into your runelite settings and replace 
  what's already there (in this case you probably wont need anything)
 in case you need to turn on the app to take screenshots and stuff, that should be the base config being used
 setup a venv using the requirements.txt in current folder, this should be enough for all tools in this repo
  the command should be: (from within this repo's directory): pip install -r requirements.txt 
  python version required is 3.10 I believe

2. next: try out some of the scripts:
2.1.1 before you start, in case running some of your bash scripts bugs out you need to run dos2unix 
 tool, this is probably because of some configuration I cant figure out, probably in git? 
  it sets line endings wrong, because it sets windows line ending, to fix this: 
 either fix this option in your git environment or run the following commands: 
  1. apt-get install dos2unix 
   to install the dos2unix tool
  2. dos2unix LocallyAvailableActionTooling/*.sh 
   to run dos2unix tool on all bash scripts
2.2
using X/XLaunch, etc.: (required such that you can receive the screen remotely)
 in case something is going wrong read the following:
  -if you bump into authority or display errors in linux, this command will most likely fix them:
   xhost +
  -if it's not working for some reason you can try starting the container manually and running it 
   like that (you can easily run it manually the command to run it is in printed out when running 
    this script)

3. screenshots, and the scraper
HOW TO TAKE SCREENSHOTS:
 you will probably want to run everything as usual, pause the running script and take screenshots
 you can also run locally and take screenshots in that way
 make sure you have 100% zoom and 100% brightness, otherwise you WILL have trouble with the screenshots
see the video tutorial on how to use the scraper
 
3.1 running the scraper:
 *the scraper allows you to get images of the several ingame artifacts (items, etc.), not everything can be obtained this way,
  sometimes you will need to go ingame and take ingame photos
 run the scraper, input the name of the item, and the item will appear at the destination you choose
 stuff to know:
  some items have multiple images:
  example: the item Zulrah's_scales found at: https://oldschool.runescape.wiki/w/Zulrah%27s_scales, has more than one image, 
   therefore, entering Zulrah's_scales in the scraper will only get you a single item
 example command: 
  python .\LocallyAvailableActionTooling\scraper.py --action_id="rs_login" --actions_repo="$git_repo_dir/runescape_actions/" run
   $git_repo_dir is your runescape_actions repo path
   -- action_id is important is the action in which the images will go to, you can find the images in: 
    all_action_files/screenshots/action/
   you can set action_id to: 0common_photos/folder_for_temp_photos so they go to a temp folder, 
    but afterwards you have to go to that folder and copy paste them into the correct place inside common photos

4. to sync your local files to your remote files, you will be using rsync (with a custom already created script):
 (you set all variables starting with $) 
 4.1 wireguard configs: after installing wireguard, just load the wireguard configs file with the wireguard app, 
  make sure you rename it, the wireguard file should not contain spaces

 4.2 ssh key: copy THE CONTENTS of priv_key.conf (the contents are what's inside the file) 
  and copy it into a file to your correct folder, if you are using wsl, 
   I advise using: /root/.ssh/priv_key , remember that file name you chose, afterwards every private 
    key should have permissions 600, therefore, just do: chmod 600 /root/.ssh/priv_key, now you can use the private key correctly
     in the following commands

 4.3 to sync files:
  in the line below you must replace your_first_name with your username on the system, which should be your first name, sync_pairs_dir, your_dev_key_path
   in the following command: 
    "folder with the repositories": folder containing the repository of runescape actions and locally available actions 
    *"your_id" is the name of the account you will be provided, which will probably be your actual first name
    *"key_path" is the path for your key, example: /root/.ssh/priv_key you created before 
   sudo rsync -avz --progress --delete-after -e "ssh -i "key_path" -o ServerAliveCountMax=3 -o ConnectTimeout=10 -o TCPKeepAlive=yes" "folder with the repositories"/ "your_id"@116.202.29.166:dev_code; 
   *the above command synchronizes your files to the remote server files
  
 TO START RUNNING YOUR ACCOUNT AND GET THE SCREEN OF THE APPLICATION BACK TO YOU:
  *notice that to get the screen back you need to have the X server running:
   you already installed (in 1. and 2.2), you need to make sure it's started, since it depends on your 
    operating system, I will leave this to you to figure out how to do this
   
  you need to send the update file, with the command:
   touch /tmp/update; sudo rsync -avz --progress --delete-after -e "ssh -i "key_path" -o ServerAliveCountMax=3 -o ConnectTimeout=10 -o TCPKeepAlive=yes" /tmp/update "your_username"@116.202.29.166:dev_code/update; rm /tmp/update 
   
  you probably just want to use the above commands together, it will sync your files and start the app for you so you get the screen back:
   sudo rsync -avz --progress --delete-after -e "ssh -i "key_path" -o ServerAliveCountMax=3 -o ConnectTimeout=10 -o TCPKeepAlive=yes" "folder with the repositories"/ "your_id"@116.202.29.166:dev_code;;touch touch /tmp/update; sudo rsync -avz --progress --delete-after -e "ssh -i "key_path" -o ServerAliveCountMax=3 -o ConnectTimeout=10 -o TCPKeepAlive=yes" /tmp/update "your_username"@116.202.29.166:dev_code/update; rm /tmp/update 
   
  *why the update file? you need to send the update file for the server to read your updated files, so always make sure to send it, whenever you  
   update your runescape_actions, in the above command there are 2 rsyncs, the first one syncs everything up, the second just sends 
    and empty file to the server, telling it to proceed with sending the code
   
4.4 How do you send your scheduler updates to the server:
  scheduler_update_in: a file in: template_scheduler_updates
  scheduler_update_out: LOCAL_DIRECTORY/scheduler_updates_dir/scheduler_update  (same as above)
  python .\LocallyAvailableActionTooling\schedule_jobs_editor.py {scheduler_update_in} {scheduler_update_out}
   where { scheduler_update_in } can be a file inside template_files:
    example: template_files/typology_of_job_manipulating_running_bot_status.json 
     (which is just a base file with all possible fields you can set in a config that manages the running state)
     there are othet types of configs you can send, configs with the next action to run for example, to pause, resume,....
   and {scheduler_update_out} is the path of the file that is the config you are sending to the server
 
run the following command to send the scheduler update
 * make sure you have seen the documentation/videos on what the scheduler is by this point
 sudo rsync -avz --progress --delete-after -e "ssh -i "key_path" -o ServerAliveCountMax=3 -o ConnectTimeout=10 -o TCPKeepAlive=yes" "scheduler_updates_folder"/ "your_username"@116.202.29.166:scheduler_updates_dir
 # recommended is: 
 scheduler_update_out: LOCAL_DIRECTORY/scheduler_updates_dir/scheduler_update  (same as above)
 actions_folder=LOCAL_DIRECTORY/runescape_actions
but you will get an idea from watching the scheduler updates video


after 15 minutes after starting the application and the bot on my system (your live run), 
 the bot will turn itself of, this is to avoid leaving it on forever, u can turn it off yourself by just shutting off the screen




