import os
import json
import random
import requests
from dotenv import load_dotenv

load_dotenv()
API_HOST = os.getenv("API_HOST")
TOKEN_WEBSHARE = os.getenv("TOKEN_WEBSHARE")
TOKEN_VIWERS = os.getenv("TOKEN_VIWERS")
TOKEN_STREAMS = os.getenv("TOKEN_STREAMS")

LOGS_PREFIX = "(api)"

class Api ():
    
    def __init__ (self):
        self.proxies = []
        
        self.__load_proxies__ ()     
        
    def __load_proxies__ (self):
        """ Query proxies from the webshare api, and save them
        """
        
        print (f"{LOGS_PREFIX} Loading proxies...")
        
        # Get proxies
        res = requests.get (
            "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=100", 
            headers = { 
                "Authorization": f"Token {TOKEN_WEBSHARE}"
            }
        )
        if res.status_code != 200:
            print (f"Error getting proxies: {res.status_code} - {res.text}")
            quit ()

        try:
            json_data = res.json ()
            self.proxies = json_data['results']
        except Exception as error:
            print (f"{LOGS_PREFIX} Error getting proxies: {error}")
            quit ()
            
    def get_users (self) -> list:
        """ users and passwords from the API

        Returns:
            dict: user data (id, username and password)
            
            Example:
            [    
                {
                    "id": 1,
                    "user": "sample 1 user",
                    "cookies": {"hello": "word"},
                },
                {
                    "id": 2,
                    "user": "sample 2 user",
                    "cookies": {"hello": "word"},
                }
            ]

        """
        
        print (f"{LOGS_PREFIX} Getting users...")
        
        # Get data from api
        res = requests.get (
            f"{API_HOST}/viwers/bots/", 
            headers={"token": TOKEN_VIWERS}
        )
        res.raise_for_status ()
        json_data = res.json ()
        
        # Validate response
        if json_data["status"] != "ok":
            print (f"{LOGS_PREFIX} Error getting users: {json_data['message']}")
            quit ()
        
        users = json_data["data"]
        
        # Filter only active users
        users = list(filter (lambda user: user["is_active"], users))
        
        # Formatd ata
        users = list(map (lambda user: {
            "id": user["id"],
            "user": user["user"],
            "cookies": user["cookies"],
        }, users))
        
        return users

    def get_proxy (self) -> dict:
        """ get a random proxy 

        Returns:
            dict: proxy data (host and port)
            
            Example:
            {
                "host": "0.0.0.0",
                "port": 80,
            }
        """
        
        print (f"{LOGS_PREFIX} Getting a random proxy...")
        
        # Get data from api
        proxy = random.choice (self.proxies)
        return {
            "host": proxy["proxy_address"],
            "port": proxy["port"],
        }

    def get_streams(self) -> list:
        """ Get current live streams in comunidad mc, using the API

        Returns:
            list: streamer names.

            Example:  ["DariDeveloper", "darideveloper2"]
        """

        print(f"{LOGS_PREFIX} Getting streams...")
        
        # Get data from api
        res = requests.get (
            f"{API_HOST}/streams/current-streams",
            headers={"token": TOKEN_STREAMS}
        )
        json_data = res.json()
        streams = json_data["data"]
        
        return streams
    
    def disable_user (self, user_id:int, user_name:str): 
        """ Disable user in the API

        Args:
            user_id (int): user id
            user_name (str): user name
        """
        
        print (f"{LOGS_PREFIX} Disabling user {user_name}...")
        
        res = requests.delete (
            f"{API_HOST}/viwers/bots/",
            headers={"token": TOKEN_VIWERS},
            json={"id": user_id},
        )
        
        json_data = res.json ()
        if json_data["status"] != "ok":
            print (f"{LOGS_PREFIX} Error disabling user: {json_data['message']}")
        
        
    # def log_error (self, error:str):
    #     """ Log error in the API

    #     Args:
    #         error (str): error message
    #     """
        
    #     url = f"{API_HOST}/log-error/?token={TOKEN}"
    #     try:
    #         res = requests.post (url, json={"error": error})
    #         res.raise_for_status()
    #     except:
    #         print ("Error saving error to API")
        
if __name__ == "__main__":
    
    api = Api ()
    users = api.get_users ()
    proxy = api.get_proxy ()
    streams = api.get_streams ()
    disabled_user = random.choice (users)
    api.disable_user (disabled_user["id"], disabled_user["user"])
    
    print ()