import os
import datetime
def say(text):
    os.system(f'say -v "Daniel" "{text}"')

def greetme():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <=12:
        say("Good Morning, Sir")
        print("Good Morning, Sir\nFriday at your service. How can i assist you today ?")
    elif hour >12 and hour <=1:
        say("Good Afternoon, Sir")
        print("Good Afternoon, Sir\nFriday at your service. How can i assist you today ?")
    else:
        say("Good Evening, Sir")
        print("Good Evening, Sir\nFriday at your service. How can i assist you today ?")

    say("Friday at your service. How can i assist you today")

