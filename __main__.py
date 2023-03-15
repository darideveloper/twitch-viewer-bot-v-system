import api
from scraper import TwitchBot

def main (): 
        
    # Get active users
    active_users = api.get_active_users()
    
    # Open scraper for each user
    for user, password in active_users.items():
        twitch_bot = TwitchBot (user, password, "https://www.twitch.tv/juansguarnizo")
        twitch_bot.login ()
        

if __name__ == "__main__":
    main()