import os
import time
import discord
from discord.ext import commands
import fire
import asyncio
from shutil import rmtree
import zipfile
import glob 
import shutil

from screenshot_tool_lib import copy_file, create_unexisting_dir
from unzip_from_discord_script import delete_any
from start_app_from_within_container_and_share_screen_script import recursive_copy_and_overwrite

'''
requirements:
    in your venv environment run, to install the required packages, run:
    pip install discord fire
     
DISCORD_BOT_TOKEN_OUTGOING is the environment variable that holds your discord api token
OUT_DATA also needs to be set to the directory where you want the zip to be extracted to
 make sure the directory exists, but it will be replaced, as soon as the zip is received

usage:
    this is meant to be used to quickly run the test on the discord server
     you have the option to provide extra arguments, like 
      an option to send to server and instantly auto run the test, and another option 
       to provide a blacklist of steps to ignore in the server, this is great when 
        paired with the autorun feature
        these arguments are the steps_to_ignore and auto_testing[y/N] (default is 'n'(no), can set to 'y')
example of running this in linux: 
 /code/venv_inside_docker/bin/python3 /opt/code/LocallyAvailableActionTooling/send_to_discord_script.py  --channel_id="1262208908991135785" --path_of_actions_folder_repo="/opt/code/runescape_actions/" --path_to_create_action_folder="/opt/temp_action_to_import/" --action_name="rs_login" --app_identifier="rs" --steps_to_ignore="1,2,3,4,5" --auto_testing="y" run
'''

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents, self_bot=True)

class UploadDiscord(object):
    def __init__(self, 
                 channel_id, 
                 path_of_actions_folder_repo,
                 action_name,
                 path_to_create_action_folder,
                 app_identifier,
                 action_dependencies=None,
                 steps_to_ignore=None,
                 actions_to_import_folder=None,
                 auto_testing='n'):
        '''
        action_dependencies: list of action names that this action depends on, this is to make sure 
         you dont send everything to discord every time 
        steps_to_ignore: list of steps to ignore in the server, these are the ints of the step 
         number
        actions_to_import_folder: a custom path to a folder where the actions are to be imported 
         from
          
        '''

        # the app identifier is the an id of the app you are using, example: 'rs' for runescape
        self.app_identifier = app_identifier
        self.create_paths_info_from_identifier(app_identifier) 

        self.actions_to_import_folder = actions_to_import_folder
        self.path_to_create_action_folder = path_to_create_action_folder
        if auto_testing.strip().lower() == 'y':
            self.is_auto_testing = True
        else:
            self.is_auto_testing = False
        if steps_to_ignore is not None:
            self.steps_to_ignore = steps_to_ignore
        else:
            self.steps_to_ignore = []
        self.channel_id = channel_id
        self.in_file_path = path_of_actions_folder_repo
        self.action_name = action_name
        if action_dependencies is not None:
            self.action_dependencies = action_dependencies
            self.action_dependencies = self.action_dependencies.split(",")
        else:
            self.action_dependencies = []

        self.env_var_discord_tkn = os.environ.get("DISCORD_BOT_TOKEN_OUTGOING")
        # self.out_data = out_data
        # self.out_data = os.environ.get("OUT_DATA")

        self.intents = discord.Intents.default()
        self.intents.messages = True
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix="/", intents=self.intents)
        self.bot.event(self.on_ready)

    def create_paths_info_from_identifier(self, app_identifier):
        if self.app_identifier == 'rs':
            self.folder_name = 'runescape_actions'
     
    async def on_ready(self):
        print(f"bot ready, channel id: {self.channel_id}, input file path: {self.in_file_path}")
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            try:
                await self.handle_send_content(channel)
            except Exception as e:
                print(f"error sending content: {e}")
        else:
            print("channel not found")
        await self.bot.close()

    async def handle_send_content(self, channel):
        # zip_file_path = '/tmp/zip_file.zip'
        zip_name = 'actions_to_import.zip' 
        if self.actions_to_import_folder is not None:
            zip_file_path = f'{self.actions_to_import_folder}/{zip_name}'
            zip_dir(self.in_file_path, zip_file_path)
        else:
            delete_any(self.path_to_create_action_folder)
            create_unexisting_dir(self.path_to_create_action_folder)
            action_folder = f'{self.path_to_create_action_folder}/{self.folder_name}/'
            create_unexisting_dir(action_folder)
            app_folder = f'{action_folder}/{self.app_identifier}/'
            create_unexisting_dir(app_folder)

            # copy over required settings files from settings folder
            src = '/root/.runelite/profiles2/default*'
            dst = f'{self.path_to_create_action_folder}/profile_info/'
            create_unexisting_dir(dst)
            for file in glob.glob(src):
                dst_to_send_file_to = os.path.join(dst, os.path.basename(file)) 
                shutil.copy(file, dst_to_send_file_to)
            src = '/root/.runelite/profiles2/profiles.json'
            dst_to_send_file_to = f'{dst}/profiles.json'
            copy_file(src, dst_to_send_file_to)

            # copy all dependencies 
            base_src = f'/opt/code/{self.folder_name}/{self.folder_name}'
            for dependency in self.action_dependencies:
                src = f'{base_src}/{dependency}/'
                dst = f'{app_folder}/{self.folder_name}/{dependency}/'
                recursive_copy_and_overwrite(src, dst)
             
            # copy base action dir
            src = f'{base_src}/{self.action_name}/'
            dst = f'{app_folder}/{self.folder_name}/{self.action_name}/'
            recursive_copy_and_overwrite(src, dst)

            src = f'/opt/code/{self.folder_name}/reusable_actions/reusable_actions' 
            dst = f'{self.path_to_create_action_folder}/common_actions/'
            create_unexisting_dir(dst)
            dst = f'{dst}/reusable_actions'
            recursive_copy_and_overwrite(src, dst)

            src = f'/opt/code/{self.folder_name}/common_action_framework/' 
            dst = f'{self.path_to_create_action_folder}/common_action_framework/' 
            recursive_copy_and_overwrite(src, dst)

            zip_file_path = f'{ self.path_to_create_action_folder }/{zip_name}'
            zip_dir(self.path_to_create_action_folder, zip_file_path)
        await channel.send(content=f'{ self.action_name }', file=discord.File(zip_file_path))
        if self.steps_to_ignore:
            # if not empty
            time.sleep(5)
            if isinstance(self.steps_to_ignore, str):
                self.steps_to_ignore = self.steps_to_ignore.split(",")
            steps_to_ignore_parsed = " ".join(map(str, self.steps_to_ignore))
            mesg_to_send = f"!filter {steps_to_ignore_parsed}"
            print(f"steps to ignore submited, sending msg: {mesg_to_send}")
            await channel.send(mesg_to_send)
        if self.is_auto_testing:
            print("auto testing option found, running !test next")
            # time.sleep(5)
            await channel.send("!test")

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.bot.start(self.env_var_discord_tkn))


def zip_dir(directory, zipname):
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".zip"):
                    continue
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))


if __name__ == "__main__":
    fire.Fire(UploadDiscord)



