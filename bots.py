import os
import random
from time import sleep
from threading import Thread
from api import Api
from bot import Bot
from dotenv import load_dotenv

load_dotenv ()

HEADLESS = os.getenv("HEADLESS") == True
VIWERS_STREAM = int(os.getenv("VIWERS_STREAM"))
WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH"))
WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT"))
SCREENSHOTS = os.getenv("SCREENSHOTS")
THREADS = int(os.getenv("THREADS"))

class BotsManager ():
    """ Watch Twitch stream with a multiple users, using cookies to login """
    
    def __init__ (self):     
        
        
        # Connect to api
        api = Api ()
        self.api = api
        
        self.streams = self.api.get_streams ()
        
        # Show error and stop when no stream founnd
        if not self.streams:
            print (f"No streams found.")
            return None
        
        self.users = self.api.get_users ()
        
        # Separator
        print ()
                
        bots_running = {}
        for stream in self.streams:
            bots_running[stream["streamer"]] = []
            
        stream_users = self.users.copy ()
        
        # Create bots to each stream
        current_stream_id = 0
        bots_total = VIWERS_STREAM*len(self.streams)
        current_bots = 0
        for _ in range(bots_total):
            
            # Get current stream
            stream = self.streams[current_stream_id]
                                                    
            # Default user
            user = {
                "name": "no-user",
                "cookies": [],
                "is_active": True
            }
            
            # Get random user
            if stream_users:
                user = random.choice (stream_users)
                stream_users.remove (user)
            
            streamer = stream["streamer"]
            try:
                bot = Bot (user["user"], user["cookies"], streamer, self.api.get_proxy(),
                        headless=HEADLESS, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                        take_screenshots=SCREENSHOTS, bots_running=bots_running[streamer])
            except Exception as e:
                error = f"{streamer} - {self.username}: Error creating bot instance: {str(e)}\n"
                print (error)
                
                # Save error details
                with open (self.log_path, "a", encoding='UTF-8') as file:
                    file.write (error)
                
                # Save error in api
                self.api.log_error (error)
                
                quit ()
                
            else:
                thread = Thread (target=self.__auto_run_bot__, args=(bot,))
                thread.start ()
                
                # Wait random time 
                sleep (random.randint (1, 10)/10)
                
                # Increase current bots
                current_bots += 1
                
                # End of threads, wait 1 minute
                if current_bots == THREADS:
                    
                    # Change stream
                    current_stream_id += 1
                    if current_stream_id == len(self.streams):
                        current_stream_id = 0
                    
                    # Wait before next bots
                    current_bots = 0
                    sleep (8)
                    print (f"\nWaiting 1 minutes before start next {THREADS} bots...\n")
                    sleep (60)
                        
        # Infinity loop to watch stream
        print ("Bot running...")
        while True:
            sleep (60)
    
    def __auto_run_bot__ (self, bot:Bot):
        """ Run single bot instance, with threading

        Args:
            bot (Bot): bot instance
        """
        
        # Random delay to start
        delay = random.randint (1, 30)/5
        sleep (delay)
        
        bot.auto_run ()
        
if __name__ == "__main__":
    # Test class
    
    BotsManager ()