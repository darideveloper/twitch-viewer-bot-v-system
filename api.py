import os
import csv

def get_active_users () -> dict:
    """ Read users from csv file and return them as dictionary

    Returns:
        dict: users active
    """
    
    users = os.path.join (os.path.dirname(__file__), "users.csv")
    with open (users, encoding="utf-8") as file:
        users = list(csv.reader (file))
    
    users_active = {}
    for user in users:
        if user[2] == "True":
            users_active[user[0]] = user[1]
    
    return users_active        
    