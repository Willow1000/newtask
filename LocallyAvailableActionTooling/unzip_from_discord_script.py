import os
import discord
from discord.ext import commands
import fire
import asyncio
from shutil import rmtree
import zipfile

'''
requirements:
    in your venv environment run, to install the required packages, run:
    pip install discord fire
     
DISCORD_BOT_TOKEN is the environment variable that holds your discord api token
OUT_DATA also needs to be set to the directory where you want the zip to be extracted to
 make sure the directory exists, but it will be replaced, as soon as the zip is received

must request discord server manager for authorization
'''

class Manager(object):
    def __init__(self, out_data=None):
        self.env_var_discord_tkn = os.environ.get("DISCORD_TOKEN")
        # self.out_data = out_data
        if out_data is not None:
            self.out_data = out_data
        else:
            # default out data
            self.out_data = '/workspace/logs/'
        self.test_bot_id = '1261803992023830608'
        self.master_id = '358340262151454721'

        self.intents = discord.Intents.default()
        self.intents.messages = True
        self.intents.message_content = True
        self.bot = commands.Bot(command_prefix="/", intents=self.intents)

        self.download_lock = asyncio.Lock()

        self.register_events()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.bot.start(self.env_var_discord_tkn))
     
    async def get_and_unzip_to_path(self, message):
        '''
        downloads the zip and extracts it into self.out_data folder
        deletes anything that previously existed in the folder
        '''
        attachment = message.attachments[0]
        # delete all that previously existed in the folder
        delete_any(self.out_data)
        os.mkdir(self.out_data)

        downloaded_zip_path = f'{ self.out_data }/received_zip.zip'
        await attachment.save(downloaded_zip_path)

        extract_path = f'{ self.out_data }/'
        async with self.download_lock:
            try:
                with zipfile.ZipFile(downloaded_zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_path)
            except Exception as e:
                print(f"error extracting zip: {e}")
        
    def register_events(self):
        @self.bot.event
        async def on_ready():
            print(f"logged in as {self.bot.user}")

        @self.bot.event
        async def on_message(message):
            current_user_id = str( message.author.id )
            if message.author == self.bot.user:
                return
            if message.author.bot:
                print(f'message from a bot with id: {current_user_id} received')
                if current_user_id == self.master_id:
                    print('message from master received')
                elif current_user_id != self.test_bot_id:
                    print('message some other bot or user received, only accepting messages from the authorized bot')
                    return
                if message.attachments and message.attachments[0].filename.endswith(".zip"):
                    print('message with zip attachment detected')
                    try:
                        await self.get_and_unzip_to_path(message)
                    except Exception as e:
                        print(f"error downloading and unzipping: {e}")
            await self.bot.process_commands(message)

def delete_any(path):
    '''
    deletes anything that exists in the path
    '''
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        rmtree(path)
    else:
        print("could not delete path: " + path + " this path doesn't exist")

if __name__ == "__main__":
    fire.Fire(Manager)


