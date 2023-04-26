import os
import random
from api import Api
from bot import Bot
from dotenv import load_dotenv

load_dotenv ()

DEBUG = os.getenv ("DEBUG") == "true"

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
        
        bots_running = {}
        for stream in self.streams:
            bots_running[stream] = []
            
        # Create bots to each stream
        for stream in self.streams:
            
            if not self.proxies:
                continue
            
            stream_users = self.users.copy ()
            
            # Only 2 users in debug mode
            if DEBUG:
                stream_users = stream_users[:2]
            
            print ("")
            print (f"Stream: {stream}\n\tstarting bots...")
            
            # Generate specific number of bots, from settings
            while len(bots_running[stream]) < self.settings["viwers-stream"]:
                                
                # Get random user
                if not stream_users:
                    print (f"\tNo more users available for this stream.")
                    break
                user = random.choice (stream_users)
                stream_users.remove (user)
                
                # Valñidate if bot started and catch error
                started = False
                while not started:
                                        
                    # Get random proxy and catch
                    proxy = self.__get_random_proxy__ ()
                    if not self.proxies:
                        print (f"\tNo more proxies available. Bot: {user['name']} stopped.")
                        break
                    
                    headless = self.settings["headless"]
                    if DEBUG:
                        headless = False
                    
                    # Create and start bot
                    bot = Bot (user["name"], user["cookies"], stream,
                            proxy["host"], proxy["port"], proxy["user"], proxy["password"],
                            timeout_stream=self.settings["timeout-min"], headless=headless, 
                            width=self.settings["window-width"], height=self.settings["window-height"])
                    started = bot.auto_run ()    
                    
                    # Detect if bot started and get status  
                    status = bot.status
                    if started:
                        break
                    
                    # Catch proxy error
                    if status == "proxy error":
                        print (f"\tBot error with proxy: {proxy['host']}:{proxy['port']}:{proxy['user']}:{proxy['password']}. Retrying...")
                        
                    if status == "cookie error":
                        print (f"\tBot error with user: {user['name']}. Update the cookies.")
                        break
                        
                if started:
                    print (f"\tBot: {bot.username} running...")
                    
                    # Save bot instance
                    bots_running[stream].append (bot) 
        
        if bots_running:
            print (f'\nBots running: ')
            for stream, bots in bots_running.items():
                print (f"\t{stream}: {len(bots)}")    
        print ()
            
    def __get_random_proxy__ (self) -> dict:
        """ Get random proxy from list and remove it

        Returns:
            dict: random proxy
        """
        
        # Validate if there are proxies free
        if not self.proxies:
            return False
        
        proxy = random.choice (self.proxies)
        self.proxies.remove (proxy)
        
        return proxy
        
if __name__ == "__main__":
    # Test class
    
    BotsManager ()