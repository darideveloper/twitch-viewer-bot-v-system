import os
import json
from threading import Thread
from time import sleep
from dotenv import load_dotenv
from scraping.web_scraping import WebScraping
from api import Api

load_dotenv ()

DEBUG = os.getenv ("DEBUG") == "true"

class Bot (WebScraping):
    """ Bot for watch Twitch stream, using cookies to login """
    
    def __init__ (self, username:str, cookies:list, user_id:int, stream:str, proxy:dict,
                  headless:bool=False, width:int=1920, height:int=1080, take_screenshots:bool=False,
                  bots_running:list=[], running_seconds:int=0, api:Api=None) -> bool:
        """ Contructor of class. Start viwer bot

        Args:
            username (str): name of user to login
            cookies (list): cookies for login, generated with chrome extension "EditThisCookie"
            stream (str): user stream to watch
            proxy (dict): list of proxies to use
            headless (bool, optional): use headless mode (hide browser). Defaults to False
            width (int, optional): width of browser window. Defaults to 1920
            height (int, optional): height of browser window. Defaults to 1080
            take_screenshots (bool, optional): take screenshots in headless mode. Defaults to False   
            bots_running (list, optional): list of bots already running. Defaults to [] 
            api (Api, optional): api connection. Defaults to None
        """
        
        # Save class variables and start browser
        self.username = username
        self.cookies = cookies
        self.user_id = user_id
        self.stream = stream
        self.proxy = proxy
        self.headless = headless
        self.width = width
        self.height = height
        self.take_screenshots = take_screenshots
        self.bots_running = bots_running
        self.running_seconds = running_seconds
        self.api = api
        
        # Urls and status
        self.twitch_url = f"https://www.twitch.tv/"
        self.twitch_url_login = f"https://www.twitch.tv/login/"
        self.twitch_url_stream = f"https://www.twitch.tv/{self.stream}"
        self.status = "running"
        
        # Css selectors
        self.selectors = {
            "twitch-login-btn": 'button[data-a-target="login-button"]',
            'start-stream-btn': 'button[data-a-target*="start-watching"]',
            "offline_status": '.home .channel-status-info.channel-status-info--offline',
            'player': '.persistent-player',           
        }
        
        # paths
        current_folder = os.path.dirname (__file__)
        self.log_path = os.path.join (current_folder, ".log")
        self.screenshots_folder = os.path.join (current_folder, "screenshots")
        self.screenshots_errors_folder = os.path.join (self.screenshots_folder, "errors")
        
        # Create folders
        os.makedirs (self.screenshots_errors_folder, exist_ok=True)
    
    def auto_run (self) -> str:
        """ Auto start browser, watch stream and close browser in background

        Returns:
            bool: True if browser started, False if not
        """
        
        print (f"({self.stream} - {self.username}) Starting bot...")
        
        # Start bot and catch load page error
        started = self.__start_bot__ ()
        if started:
            
            # Save bot in list of bots running
            self.bots_running.append (self)
            
            print (f"\t({self.stream} - {self.username}) Bot running (total bots in all stream: {len (self.bots_running)})")
            
            # Start tread for kill chrome when stream ends
            thread = Thread (target=self.__kill_bot__, args=())
            thread.start ()
            
        else:
            # Force end bot
            self.driver.quit ()
                
    def __load_twitch__ (self) -> bool:
        """ Try to load twitch page and validate if proxy is working

        Returns:
            bool: True if twitch load, else False
        """
        
        try:
            self.set_page ("http://ipinfo.io/json")
            self.set_page (self.twitch_url_login)
            self.refresh_selenium ()
        except:
            return False
        else:
            return True
    
    def __set_quality_mute__ (self): 
        """ Set video quality to lower and mute stream, with local storage """
        
        try:
            self.set_local_storage ("video-quality", '{"default":"160p30"}')
            self.set_local_storage ("volume", "0")
        except:
            pass
    
    def __start_bot__ (self) -> bool:
        """ Start browser and watch stream

        Returns:
            bool: True if browser started, False if not
        """
            
        browser_opened = False
        error = ""
        for _ in range (2):
            # Try to start chrome
            try:
                super().__init__ (headless=self.headless, time_out=30,
                                proxy_server=self.proxy["host"], proxy_port=self.proxy["port"],
                                width=self.width, height=self.height)
            except Exception as e:
                error = e
                print (f"\t({self.stream} - {self.username}), error opening browser, trying again in 1 minute...")
                sleep (60)
                continue
            else:
                browser_opened = True
                break
            
        if not browser_opened:
            error = f"\t({self.stream} - {self.username}): error opening browser, and max retries reached: ({error})"
            print (error)
            
            # Save error details
            with open (self.log_path, "a", encoding='UTF-8') as file:
                file.write (error)
            
            quit ()

        proxy_working = self.__load_twitch__ ()    
        
        if not proxy_working:
            error = f"\t({self.stream} - {self.username}) proxy error: {self.proxy['host']}:{self.proxy['port']}. Retrying..."
            print (error)
            return False
            
        # Load cookies
        if self.username != "no-user":
            self.set_cookies (self.cookies)
            self.__set_quality_mute__ ()
        
        # Open stream
        try:
            self.set_page (self.twitch_url_stream)
        except Exception as e:
            error = f"\t({self.stream} - {self.username}) proxy error: {self.proxy['host']}:{self.proxy['port']} bot"
            return False
        
        # Validte session with cookies
        login_button = self.get_elems (self.selectors["twitch-login-btn"])
        if login_button and self.username != "no-user":
            error = f"\t({self.stream} - {self.username}) cookie error"
            print (error)
            
            # Disable user in backend
            self.api.disable_user (self.user_id, self.username)
            
            return False
        
         # Check if stream is offline
        self.refresh_selenium ()
        offline_status = self.get_elems (self.selectors["offline_status"])
        if offline_status:
            error = f"\t({self.stream} - {self.username}) stream offline"
            print (error)
            
            return False
        
        # Accept mature content
        start_stream_elem = self.get_elems (self.selectors["start-stream-btn"])
        if start_stream_elem:
            self.click_js (self.selectors["start-stream-btn"])
            sleep (5)
            self.refresh_selenium ()
    
        # Hide video
        player = self.get_elems (self.selectors["player"])
        if player:
            script = f"document.querySelector ('{self.selectors['player']}').style.display = 'none'"
            self.driver.execute_script (script)
    
        # Take screenshot
        if self.take_screenshots:
            screenshot_path = os.path.join(self.screenshots_folder, f"{self.stream} - {self.username}.png")
            self.screenshot (screenshot_path)
        
        return True
        
    def __kill_bot__ (self): 
        
        sleep (abs(self.running_seconds))
        print (f"\t({self.stream} - {self.username}) Killing bot...")
        self.end_browser ()