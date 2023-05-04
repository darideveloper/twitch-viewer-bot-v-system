import os
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor

from api import Api
from bot import Bot

from dotenv import load_dotenv

load_dotenv ()

DEBUG = os.getenv ("DEBUG") == "true"
DEBUG_USERS = os.getenv ("DEBUG_USERS")
if DEBUG_USERS and DEBUG_USERS != "":
    DEBUG_USERS = DEBUG_USERS.split (",")
DIABLE_THREADS = os.getenv ("DIABLE_THREADS") == "true"

class BotsManager ():
    """ Watch Twitch stream with a multiple users, using cookies to login """
    
    def __init__ (self):     
        
        
        # Connect to api
        api = Api ()
        
        self.streams = api.get_streams ()
        
        # Show error and stop when no stream founnd
        if not self.streams:
            print (f"No streams found.")
            return None
        
        self.users = api.get_users ()
        self.settings = api.get_settings ()
        self.proxies = api.get_proxies ()
        
        # Separator
        print ()
        
        # Create threads executor
        executor = ThreadPoolExecutor(max_workers=self.settings["threads"])
        
        bots_running = {}
        for stream in self.streams:
            bots_running[stream] = []
            
        # Create bots to each stream
        for stream in self.streams:
            
            if not self.proxies:
                continue
            
            stream_users = self.users.copy ()
            
            # Only 2 users in debug mode
            stream_users = stream_users
                        
            # Generate specific number of bots, from settings
            while len(bots_running[stream]) < self.settings["viwers-stream"]:
                                
                # Get random user
                if not stream_users:
                    break
                user = random.choice (stream_users)
                stream_users.remove (user)
                
                # Debug options
                headless = self.settings["headless"]
                if DEBUG:
                    
                    # Force headless mode
                    headless = False
                
                    # Only start debug users
                    if DEBUG_USERS and user["name"] not in DEBUG_USERS:
                        continue
                
                try:
                    bot = Bot (user["name"], user["cookies"], stream, self.proxies,
                            timeout_stream=self.settings["timeout-min"], headless=headless, 
                            width=self.settings["window-width"], height=self.settings["window-height"],
                            take_screenshots=self.settings["screenshots"], bots_running=bots_running[stream])
                except Exception as e:
                    error = f"\t({self.stream} - {self.username}) error creating bot"
                    print (error)
                    
                    # Save error details
                    with open (self.log_path, "a", encoding='UTF-8') as file:
                        file.write (f"{self.stream} - {self.username}: {str(e)}\n")
                    
                else:
                    # Start bot in a thread if no error
                    if DIABLE_THREADS:
                        bot.auto_run ()
                    else:
                        executor.submit (self.__auto_run_bot__, bot) 
    
    def __auto_run_bot__ (self, bot:Bot):
        """ Run single bot instance, with threading

        Args:
            bot (Bot): bot instance
        """
        
        # Random delay to start
        delay = random.randint (1, 30)
        sleep (delay/10)
        
        bot.auto_run ()
        
if __name__ == "__main__":
    # Test class
    
    BotsManager ()