import re
from bs4 import BeautifulSoup
import requests
from datetime import datetime

greetings = ['greetings', 'hi', 'hello', 'hey', 'howdy']
define = ['define', 'explain', 'describe']
exits = ['exit', 'leave', 'leave', 'close']
print("FRIDAY: Hello User! My Name is Friday. I am a General Purpose Chatbot.")

while True:
    user_input = input("USER: ").lower()
    print("FRIDAY: ", end='')
    # greet the user back
    if re.search('|'.join(greetings), user_input) is not None:
        print(user_input.split(' ')[0].capitalize() + "! How May I Assist You Today?")
    # search wikipedia and define the term user wants
    elif re.search('|'.join(define), user_input) is not None:
        term = user_input.split(' ')[-1]
        page = requests.get("https://en.wikipedia.org/wiki/" + term)
        soup = BeautifulSoup(page.content, 'html.parser')
        print(soup.find_all('p')[1].get_text())
    # give user the time
    elif re.search('time', user_input) is not None:
        t = datetime.now().time()
        h = t.hour
        if h == 0:
            print("The Time is " + "12:" + str(t.minute) + "AM")
        elif t.hour < 12:
            print("The Time is " + str(h) + ":" + str(t.minute) + "AM")
        elif t.hour == 12:
            print("The Time is " + "12:" + str(t.minute) + "PM")
        else:
            print("The Time is " + str(h - 12) + ":" + str(t.minute) + "PM")
    # give user the date
    elif re.search('date', user_input) is not None:
        t = datetime.now().date()
        print("The Date is " + str(t))
    # get current world news
    elif re.search('news', user_input) is not None:
        response = requests.get('https://www.bbc.com/news')
        soup = BeautifulSoup(response.text, 'html.parser')
        for p in soup.find('body').find_all('p')[:10]:
            print(p.text.strip())
    # exit the conversation
    elif re.search('|'.join(exits), user_input) is not None:
        print("Your Welcome for the Assistance. Exiting......")
        break
    print("FRIDAY: Anything Else?")
