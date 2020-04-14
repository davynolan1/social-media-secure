import json
import sys
import cryptography
from cryptography.fernet import Fernet
from api_keys import CONSUMER_KEY, CONSUMER_SECRET, KEY, SECRET
import tweepy

f = open("user-group.txt", "r")
secure_group = f.read().splitlines()
try:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(KEY, SECRET)
    api = tweepy.API(auth)
    current_user = api.me().screen_name
except:
    print("Error: Please enter your API keys into api_keys.py file.")
    exit(0)



def secure_user(username):
    if username in secure_group:
        return True
    return False

def create_encrypt_key():
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key)
    file.close()

def read_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key

def encrypt_tweet(tweet):
    text = tweet.text.encode()
    f = Fernet(read_key())
    return f.encrypt(text)
    
def encrypt_check(tweet):
    print(bcolors.FAIL+"@"+bcolors.BOLD+bcolors.OKBLUE+tweet.user.screen_name+bcolors.ENDC+":")
    if(secure_user(tweet.user.screen_name) and not(secure_user(current_user))):
        return encrypt_tweet(tweet)
    return tweet.text

def display_user_tl(username):
    print(username)
    try:
        for tweet in api.user_timeline(username):
            print(encrypt_check(tweet))
            print()
    except:
        print(bcolors.BOLD+bcolors.FAIL+"User does not exist."+bcolors.ENDC)

def display_home_tl():
    for tweet in api.home_timeline():
        print(encrypt_check(tweet))
        print()

def tweet_text(text):
    try:
        api.update_status(text)
        print(bcolors.BOLD+bcolors.OKGREEN+"Tweet successfully posted."+bcolors.ENDC)
    except:
        print(bcolors.BOLD+bcolors.FAIL+"Tweet failed to post."+bcolors.ENDC)

    
def update_secure_group():
    f = open("user-group.txt", "r")
    secure_group = f.read().splitlines()

def display_sec_group():
    print(bcolors.BOLD + bcolors.UNDERLINE + bcolors.OKBLUE+"\nSecure Group Members:"+bcolors.ENDC)
    for user in secure_group:
        print(user)

def add_to_sec_group(username):
    filename = "user-group.txt"
    if secure_user(username):
        print(bcolors.BOLD +bcolors.FAIL+username+" is already in Secure Group."+ bcolors.ENDC)
        return
    bl= open(filename,'a')
    try:
        bl.write(username+"\n")
        print(bcolors.BOLD +bcolors.OKGREEN+"Successfully added "+username+" to Secure Group."+ bcolors.ENDC)
    except:
        print(bcolors.BOLD +bcolors.FAIL+"Failed to add "+username+" to Secure Group."+ bcolors.ENDC)
    bl.close()
    update_secure_group()

def rem_from_sec_group(username):
    filename = "user-group.txt"
    is_in_list = 0
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except:
        print(bcolors.BOLD +bcolors.FAIL+"Error: Could not open "+filename+"."+ bcolors.ENDC)

    try:
        with open(filename, "w") as f:
            for line in lines:
                if line.strip("\n") != username:
                    f.write(line)
                if line.strip("\n") == username:
                    is_in_list =1
        f.close()
    except:
        print(bcolors.BOLD +bcolors.FAIL+"Error: Could not open "+filename+"."+ bcolors.ENDC)
    if(is_in_list == 0):
        print(bcolors.BOLD +bcolors.FAIL+username, "is not in Secure Group so cannot be removed."+bcolors.ENDC)
    elif(is_in_list == 1):
        print(bcolors.BOLD +bcolors.OKGREEN+ username,"successfully removed from Secure Group"+ bcolors.ENDC)
   
    update_secure_group()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def ui_main_menu():
    print(bcolors.BOLD + bcolors.OKBLUE+"\n*********************************************************"+ bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKBLUE+"* Welcome to the Secure Twitter Encryption Application! *"+ bcolors.ENDC)
    print(bcolors.BOLD + bcolors.OKBLUE+"*********************************************************"+ bcolors.ENDC)

    print("\n"+bcolors.BOLD +bcolors.OKGREEN+"1."+bcolors.ENDC+" View Home Timeline")
    print(bcolors.BOLD +bcolors.OKGREEN+"2."+bcolors.ENDC+" View User Timeline")
    print(bcolors.BOLD +bcolors.OKGREEN+"3."+bcolors.ENDC+" Post Tweet")
    print(bcolors.BOLD +bcolors.OKGREEN+"4."+bcolors.ENDC+" Secure Group Options")
    print(bcolors.BOLD +bcolors.OKGREEN+"e."+bcolors.ENDC+" Exit Application\n")

    try:
        option = input("What would you like to do?"+ bcolors.BOLD +bcolors.OKGREEN+"(Enter option number)\n"+bcolors.ENDC)

        if(option == '1'):
            display_home_tl()
            go_back = input(bcolors.BOLD +bcolors.OKGREEN+"Go back to main menu? (y/n): "+bcolors.ENDC)
            if(go_back == 'y'):
                ui_main_menu()
            else:
                print(bcolors.BOLD+bcolors.OKGREEN+"\nGoodbye."+bcolors.ENDC)
                return

        if(option == '2'):
            username = input(bcolors.BOLD +"Enter username to view their timeline: "+ bcolors.ENDC)
            display_user_tl(username)
            go_back = input(bcolors.BOLD +bcolors.OKGREEN+"Go back to main menu? (y/n): "+bcolors.ENDC)
            if(go_back == 'y'):
                ui_main_menu()
            else:
                print(bcolors.BOLD+bcolors.OKGREEN+"\nGoodbye."+bcolors.ENDC)
                return

        if(option == '3'):
            text = input(bcolors.BOLD +"Enter text of tweet you wish to post: "+ bcolors.ENDC)
            tweet_text(text)
            go_back = input(bcolors.BOLD +bcolors.OKGREEN+"Go back to main menu? (y/n): "+bcolors.ENDC)
            if(go_back == 'y'):
                ui_main_menu()
            else:
                print(bcolors.BOLD+bcolors.OKGREEN+"\nGoodbye."+bcolors.ENDC)
                return
        
        if(option == '4'):
            ui_sec_group()
       
        if(option == 'e'):
            print(bcolors.BOLD+bcolors.OKGREEN+"\nGoodbye."+bcolors.ENDC)
            return

    except KeyboardInterrupt:
        print(bcolors.BOLD+bcolors.OKGREEN+"\nGoodbye."+bcolors.ENDC)

def ui_sec_group():
    if secure_user(current_user):   
        print(bcolors.BOLD + bcolors.UNDERLINE + bcolors.OKBLUE+"\nSecure Group Options"+ bcolors.ENDC)
        print("\n"+bcolors.BOLD +bcolors.OKGREEN+"1."+bcolors.ENDC+" View Secure Group Members")
        print(bcolors.BOLD +bcolors.OKGREEN+"2."+bcolors.ENDC+" Add User to Secure Group")
        print(bcolors.BOLD +bcolors.OKGREEN+"3."+bcolors.ENDC+" Remove User from Secure Group")
        print(bcolors.BOLD +bcolors.OKGREEN+"e."+bcolors.ENDC+" Go back\n")

        try:
            option = input("What would you like to do?"+ bcolors.BOLD +bcolors.OKGREEN+"(Enter option number)\n"+bcolors.ENDC)

            if(option == '1'):
                display_sec_group()

            if(option == '2'):
                display_sec_group()
                username = input(bcolors.BOLD +"Enter username you wish to add to Secure Group: "+ bcolors.ENDC)
                add_to_sec_group(username)
            
            if(option == '3'):
                display_sec_group()
                username = input(bcolors.BOLD +"Enter username you wish to remove from Secure Group: "+ bcolors.ENDC)
                rem_from_sec_group(username)
            
            if(option == 'e'):
                ui_main_menu()

        except KeyboardInterrupt:
            print (bcolors.BOLD+bcolors.OKGREEN+"\nGoodbye."+bcolors.ENDC)
    else:
        print(bcolors.BOLD +bcolors.FAIL+"Access restriced; current user is not in Secure Group."+bcolors.ENDC)
    
    
    

if __name__ == "__main__":
    create_encrypt_key()
    print("Current user: " + current_user)
    if(len(secure_group) == 0):
        add_to_sec_group(current_user)
    ui_main_menu()

  
