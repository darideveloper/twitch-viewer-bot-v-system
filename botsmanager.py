import os
from api import Api
from scraping_manager.automate import WebScraping

class BotsManager (WebScraping):
    """ Watch Twitch stream with a multiple users, using cookies to login """
    
    def __init__ (self):     
        
        # Connect to api
        api = Api ()
        
        self.users = api.get_users ()
        self.settings = api.get_settings ()
        self.proxies = api.get_proxies ()
        self.streams = api.get_streams ()
        
        
if __name__ == "__main__":
    # Test class
    
    BotsManager ()
    
    