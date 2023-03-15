import os
from scraping_manager.automate import WebScraping

class TwitchBot (WebScraping):
    """"""
    
    def __init__ (self, user, password, stream_link):
        """ Constructor for TwitchBot

        Args:
            user (str): twitch user for login
            password (str): twitch password for login
            stream_link (str): twitch stream link
        """
        
        self.user = user
        self.password = password
        self.stream_link = stream_link
        self.login_link = "https://www.twitch.tv/login"
        self.chrome_folder = os.path.join (os.path.dirname(__file__), "chrome_data", "User Data")
        
        self.selectors = {
            "login_user": "#login-username",
            "login_password": "#password-input", 
            "login_submit": 'button[data-a-target="passport-login-button"]'
        }
        
        # Open browser
        super().__init__ (chrome_folder=self.chrome_folder)
        
    def login (self, wait_login=True):
        """ Login to twitch account

        Args:
            wait_login (bool, optional): Wait after submit email and password. Defaults to True.
        """
        
        # Load login page
        self.set_page (self.login_link)
        
        # Login
        self.send_data (self.selectors["login_user"], self.user)
        self.send_data (self.selectors["login_password"], self.password)
        self.click_js (self.selectors["login_submit"])
        
        # Wait for manual login required
        if wait_login:
            input (f"Usuario: {self.user}. Enter para continuar...")
    
    