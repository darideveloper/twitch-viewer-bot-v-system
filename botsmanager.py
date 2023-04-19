import os
import random
from api import Api
from bot import Bot
from threading import Thread

class BotsManager ():
    """ Watch Twitch stream with a multiple users, using cookies to login """
    
    def __init__ (self):     
        
        # Connect to api
        api = Api ()
        
        self.users = api.get_users ()
        self.settings = api.get_settings ()
        self.proxies = api.get_proxies ()
        self.streams = api.get_streams ()
        
        bots_running = {}
        
        # Create bots to each stream
        for stream in self.streams:
            
            stream_users = self.users.copy ()
            
            print (f"Stream: {stream}")
            
            # Generate specific number of bots, from settings
            for _ in range (self.settings["viwers_stream"]):
                
                # Get random user
                user = random.choice (stream_users)
                stream_users.remove (user)
                
                # Get random proxy
                proxy = random.choice (self.proxies)
                self.proxies.remove (proxy)
                
                # Create bot
                bot = Bot (user["name"], user["cookies"], stream,
                           proxy["host"], proxy["port"], proxy["user"], proxy["password"],
                           timeout=10)
                
                print (f"\tBot: {bot.username} running...")
                
                # Save bot instance
                if stream not in bots_running:
                    bots_running[stream] = [bot]
                else:
                    bots_running[stream].append (bot) 
                
            print (f'\tBots running: {self.settings["viwers_stream"]}')           
        
        
if __name__ == "__main__":
    # Test class
    
    BotsManager ()
    
    