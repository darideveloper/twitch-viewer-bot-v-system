import os
import requests
from dotenv import load_dotenv

load_dotenv ()
API_HOST = os.getenv ("API_HOST")
API_KEY = os.getenv ("API_KEY")

class Api ():
    
    def get_users (self) -> list:
        """ Get twitch user for the bot, using the API

        Returns:
            list: list of dictionaries with user data
            
            Example: 
            [
                {
                    "name": "DariDeveloper",
                    "cookies": [...],
                    "is_active": true,
                    "last_update": "2023-04-17T23:29:07.083Z"
                }
                ...
            ]
        """
        
        # Get data from api
        url = f"{API_HOST}/users/"
        res = requests.get (url)
        users = res.json ()
        
        # filter active users
        users = list(filter(lambda user: user["fields"]["is_active"], users))
        
        # Format users
        users = list(map(lambda user: user["fields"], users))
        
        return users
    
    def get_settings (self) -> list:
        """ Get settings for the bot, using the API

        Returns:
            list: dictionary with settings data
            
            Example: {"viwers_stream": 20}
        """
        
        # Get data from api
        url = f"{API_HOST}/settings/"
        res = requests.get (url)
        settings = res.json ()
    
        # Format settings
        setting_formatted = {}
        for setting in settings:
            key = setting["fields"]["name"]
            value = setting["fields"]["value"]
            
            # Convert values to int if possible
            if value.isdigit ():
                value = int (value)
            
            setting_formatted[key] = value
            
        return setting_formatted
    
    def get_proxies (self) -> list:
        """ Get proxies for the bot, using the API

        Returns:
            list: list of dictionaries with proxy data
            
            Example:
            [
                {
                    "host": "123.123.123.123",
                    "port": 80,
                    "user": "my user",
                    "password": "my password",
                    "location": 1
                }
                ...
            ]
        """
        
        # Get data from api
        url = f"{API_HOST}/proxies/"
        res = requests.get (url)
        proxies = res.json ()
        
        # Format proxies
        proxies = list(map(lambda proxy: proxy["fields"], proxies))
        
        return proxies
    
    def get_streams (self) -> dict:
        """ Get current live streams in comunidad mc, using the API

        Returns:
            dict: streamer names.
            
            Example:  ["DariDeveloper", "darideveloper2"]
        """
        
        # Get data from api
        url = f"{API_HOST}/streams/"
        res = requests.get (url)
        return res.json ()
    
    
    