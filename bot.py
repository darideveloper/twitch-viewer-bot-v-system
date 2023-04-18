import json
from time import sleep
from threading import Thread
from scraping_manager.automate import WebScraping

class Bot (WebScraping):
    """ Bot for watch Twitch stream, using cookies to login """
    
    def __init__ (self, username:str, cookies:list, stream:str,
                  proxy_host:str, proxy_port:int, proxy_user:str="", proxy_pass:str="",
                  headless:bool=False, timeout:int=60):
        """ Contructor of class. Start viwer bot

        Args:
            username (str): name of user to login
            cookies (list): cookies for login, generated with chrome extension "EditThisCookie"
            stream (str): user stream to watch
            proxy_host (str): proxy host
            proxy_port (int): proxy port
            proxy_user (str, optional): proxy user. Defaults to ""
            proxy_pass (str, optional): proxy password. Defaults to ""
            headless (bool, optional): use headless mode (hide browser). Defaults to False
            timeout (int, optional): time to wait (in minutes) before close browser. Defaults to 60
        """
        
        # Save class variables and start browser
        self.username = username
        self.cookies = cookies
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        self.headless = headless
        self.stream = stream
        self.timeout = timeout
        self.twitch_url = f"https://www.twitch.tv/"
        self.twitch_stream = f"https://www.twitch.tv/{self.stream}"
        self.status = "running"
        
        # Start thread for start browser in background
        therad_start_browser = Thread (target=self.__start_bot__)
        therad_start_browser.start ()
        
        # Start thread for close browser in background
        therad_end_browser = Thread (target=self.__end_bot__)
        therad_end_browser.start ()
        
        while True:
            print (self.status)
            sleep (1)
            
    def __start_bot__ (self):
        """ Start browser and watch stream """
        
        
        super ().__init__ (self.twitch_url, self.headless, 
                           proxy_server=self.proxy_host, proxy_port=self.proxy_port,
                           proxy_user=self.proxy_user, proxy_pass=self.proxy_pass,
                           cookies=self.cookies)
        
        self.set_page (self.twitch_stream)
        
    def __end_bot__ (self):
        """ Close when time out end """
        
        timeout_seconds = self.timeout * 60
        sleep (timeout_seconds)
        
        self.status = "ended"        
        self.driver.quit ()

        
if __name__ == "__main__":
    
    # Test class
    cookies_json = """[{"id": 1, "name": "api_token", "path": "/", "value": "7ba5cab4ca07322c9803c7151483f07c", "domain": ".twitch.tv", "secure": true, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "unspecified", "expirationDate": 1696216775.896431}, {"id": 2, "name": "auth-token", "path": "/", "value": "xvb4ei69yqexvkwenmw30vvy07hxje", "domain": ".twitch.tv", "secure": true, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "no_restriction", "expirationDate": 1682378752.10728}, {"id": 3, "name": "experiment_overrides", "path": "/", "value": "{%22experiments%22:{}%2C%22disabled%22:[]}", "domain": ".twitch.tv", "secure": true, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "no_restriction", "expirationDate": 1682378741.012931}, {"id": 4, "name": "last_login", "path": "/", "value": "2023-04-05T03:19:35Z", "domain": ".twitch.tv", "secure": false, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "unspecified", "expirationDate": 1696216775.896358}, {"id": 5, "name": "login", "path": "/", "value": "darideveloper", "domain": ".twitch.tv", "secure": true, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "no_restriction", "expirationDate": 1682378752.108888}, {"id": 6, "name": "name", "path": "/", "value": "darideveloper", "domain": ".twitch.tv", "secure": false, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "unspecified", "expirationDate": 1696216775.896309}, {"id": 7, "name": "persistent", "path": "/", "value": "733167917%3A%3Acfiyupyk2d7rg7j55kmuip4aw9807q", "domain": ".twitch.tv", "secure": true, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": true, "sameSite": "unspecified", "expirationDate": 1696216775.896054}, {"id": 8, "name": "server_session_id", "path": "/", "value": "73d10f1f2fab4c54ac25bb5f223082d9", "domain": ".twitch.tv", "secure": true, "session": true, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "no_restriction"}, {"id": 9, "name": "twilight-user", "path": "/", "value": "{%22authToken%22:%22xvb4ei69yqexvkwenmw30vvy07hxje%22%2C%22displayName%22:%22DariDeveloper%22%2C%22id%22:%22733167917%22%2C%22login%22:%22darideveloper%22%2C%22roles%22:{%22isStaff%22:false}%2C%22version%22:2}", "domain": ".twitch.tv", "secure": true, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "no_restriction", "expirationDate": 1682378752.106637}, {"id": 10, "name": "twitch.lohp.countryCode", "path": "/", "value": "MX", "domain": ".twitch.tv", "secure": false, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "unspecified", "expirationDate": 1697325955.778201}, {"id": 11, "name": "unique_id", "path": "/", "value": "KZrp6q8EJWPbyyFKHoHHu1hzVXkDXD1s", "domain": ".twitch.tv", "secure": true, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": false, "sameSite": "no_restriction", "expirationDate": 1697325940.182774}, {"id": 12, "name": "unique_id_durable", "path": "/", "value": "KZrp6q8EJWPbyyFKHoHHu1hzVXkDXD1s", "domain": ".twitch.tv", "secure": true, "session": false, "storeId": "0", "hostOnly": false, "httpOnly": true, "sameSite": "no_restriction", "expirationDate": 1697325940.18284}]"""
    
    BotsManager (
        cookies=json.loads (cookies_json), 
        stream="darideveloper", 
        proxy_host="p.webshare.io", 
        proxy_port=80, 
        proxy_user="gxqupdei-US-1", 
        proxy_pass="44590csz5uyn" , 
        headless=False, 
        timeout=0.5
    )
    
    