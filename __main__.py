import api
from viwerbot import ViwerBot
from threading import Thread

def main (): 
        
    # # Get active users
    # active_users = api.get_active_users()
    
    # # Start scrapers and crate chrome data folders
    # threads = []
    # for user, password in active_users.items():
    #     twitch_bot = ViwerBot (user, password, "https://www.twitch.tv/juansguarnizo")
    #     threads.append(Thread (target=twitch_bot.auto_run))
        
    # # Start threads
    # for thread in threads:
    #     thread.start()
    
    ViwerBot ()

if __name__ == "__main__":
    main()