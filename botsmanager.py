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
            
            if not self.proxies:
                continue
            
            stream_users = self.users.copy ()
            
            print (f"Stream: {stream}")
            
            # Generate specific number of bots, from settings
            for _ in range (self.settings["viwers_stream"]):
                
                # Get random user
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
                    
                    # Create and start bot
                    bot = Bot (user["name"], user["cookies"], stream,
                            proxy["host"], proxy["port"], proxy["user"], proxy["password"],
                            timeout_stream=10)
                    started = bot.auto_run ()    
                    
                    # Detect if bot started and get status  
                    status = bot.status
                    if started:
                        break
                    
                    # Catch proxy error
                    if status == "proxy error":
                        print (f"\tPage not loaded with proxy: {proxy['host']}:{proxy['port']}:{proxy['user']}:{proxy['password']}. Retrying...")
                        
                        
            
                print (f"\tBot: {bot.username} running...")
                
                # Save bot instance
                if stream not in bots_running:
                    bots_running[stream] = [bot]
                else:
                    bots_running[stream].append (bot) 
                
            print (f'\tBots running: {self.settings["viwers_stream"]}')           
        
    def __get_random_proxy__ (self) -> dict:
        """ Get random proxy from list and remove it

        Returns:
            dict: random proxy
        """
        
        # Validate if there are proxies
        if not self.proxies:
            return False
        
        proxy = random.choice (self.proxies)
        self.proxies.remove (proxy)
        
        return proxy
        
if __name__ == "__main__":
    # Test class
    
    BotsManager ()
    
    