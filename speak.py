import JarvisAI
import os
import re
import pprint
import random
import warnings
from bs4 import BeautifulSoup
import requests
import re
import integrate
from textblob import TextBlob as tb

warnings.filterwarnings("ignore")
warnings.warn("second example of warning!")

obj = JarvisAI.JarvisAssistant()


def t2s(text):
    obj.text2speech(text)


def start(x):

    integrate.ChatApplication._insert_message(x,"Listening","Assistant")
    
    res = obj.mic_input()

    blob = tb(res)
    sent=blob.sentiment.polarity
    # integrate.ChatApplication._insert_message(x,blob.sentiment.polarity,"sentiment")
    print("sentiment : "+str(sent))        
        

    if re.search("jokes|joke|Jokes|Joke", res):
        joke_ = obj.tell_me_joke('en', 'neutral')
        integrate.ChatApplication._insert_message(x,res,"You")
        integrate.ChatApplication._insert_message(x,joke_,"Assistant")
        t2s(joke_)

    elif re.search('setup|set up', res):
        setup = obj.setup()
        print(setup)

    elif re.search('google photos', res):
        photos = obj.show_google_photos()
        print(photos)

    elif re.search('local photos', res):
        photos = obj.show_me_my_images()
        print(photos)

    elif re.search('weather|temperature', res):
        city = res.split(' ')[-1]
        weather_res = obj.weather(city=city)
        integrate.ChatApplication._insert_message(x,res,"You")
        integrate.ChatApplication._insert_message(x,weather_res,"Assistant")
        t2s(weather_res)

    elif re.search('news', res):
        news_res = obj.news()
        for i in range(len(news_res)):
            integrate.ChatApplication._insert_message(x,news_res[i],"Assistant")
                
        t2s(f"I have found {len(news_res)} news. You can read it. Let me tell you first 2 of them")
        t2s(news_res[0])
        t2s(news_res[1])

    elif re.search('tell me about', res):
        topic = res[14:]
        integrate.ChatApplication._insert_message(x,res,"You")
        wiki_res = obj.tell_me(topic, sentences=1)
        integrate.ChatApplication._insert_message(x,wiki_res,"Assistant")
        t2s(wiki_res)

    elif re.search('recommend movies',res):
        url = 'http://www.imdb.com/chart/top'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        movies = soup.select('td.titleColumn')
        links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
        crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
        ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
        votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

        imdb = []

                    # Store each item into dictionary (data), then put those into a list (imdb)
        for index in range(0, len(movies)):
                        # Seperate movie into: 'place', 'title', 'year'
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index))+1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            place = movie[:len(str(index))-(len(movie))]
            data = {"movie_title": movie_title,"year": year,
                                    "place": place,
                                    "star_cast": crew[index],
                                    "rating": ratings[index],
                                    "vote": votes[index],
                                    "link": links[index]}
            imdb.append(data)
        imdb_1= imdb[0:11]
        integrate.ChatApplication._insert_message(x,res,"You")
        for item in imdb_1:
            ans=(item['place']+ '-'+ item['movie_title']+ '('+item['year']+') -'+ 'Starring:'+ item['star_cast'])
            integrate.ChatApplication._insert_message(x,ans,"Assistant") 

    elif re.search('date', res):
        integrate.ChatApplication._insert_message(x,res,"You")
        date = obj.tell_me_date()
        (t2s(date))
        integrate.ChatApplication._insert_message(x,date,"Assistant")



    elif re.search('flipkart', res):
        search_item = res.split()
        search_item="+".join(search_item)
        url = 'https://www.flipkart.com/search?q='+search_item+'&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
        response=requests.get(url)
        soup=BeautifulSoup(response.content,'lxml')
        integrate.ChatApplication._insert_message(x,res,"You")
        for item in soup.select('[data-id]'):
          try:
            integrate.ChatApplication._insert_message(x,'----------------------------------------',"")
            #print(item)
            integrate.ChatApplication._insert_message(x,item.select('a img')[0]['alt'],"Assistant")
            integrate.ChatApplication._insert_message(x,item.select('[id*=productRating]')[0].get_text().strip(),"Assistant")
            prices = item.find_all(text=re.compile('₹')) 
            integrate.ChatApplication._insert_message(x,prices[0],"Assistant")
            discounts = item.find_all(text=re.compile('off')) 
            integrate.ChatApplication._insert_message(x,discounts[0],"Assistant")
          except Exception as e:
            #raise e
            b=0


            
    # elif re.search('amazon', res):
    #                 search_item = res.split()
    #                 search_item="+".join(search_item)
    #                 url = 'https://www.amazon.in/s?k='+search_item+'&ref=nb_sb_noss_2'
    #                 response=requests.get(url)
    #                 soup=BeautifulSoup(response.content,'lxml')
    #                 for item in soup.select('[data-id]'):
    #                   try:
    #                     print('----------------------------------------')
    #                     #print(item)
    #                     print(item.select('a img')[0]['alt'])
    #                     print(item.select('[id*=productRating]')[0].get_text().strip())
    #                     prices = item.find_all(text=re.compile('₹')) 
    #                     print(prices[0])
    #                     discounts = item.find_all(text=re.compile('off')) 
    #                     print(discounts[0])
    #                   except Exception as e:
    #                     #raise e
    #                     b=0    


    elif re.search('time', res):
        time = obj.tell_me_time()
        print(time)
        t2s(time)

    elif re.search('open', res):
        domain = res.split(' ')[-1]
        open_result = obj.website_opener(domain)
        print(open_result)

    elif re.search('launch', res):
        dict_app = {
            'chrome': 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            'epic games': 'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe'
        }

        app = res.split(' ', 1)[1]
        path = dict_app.get(app)
        integrate.ChatApplication._insert_message(x,res,"You")
        if path is None:
            t2s('Application path not found')
            integrate.ChatApplication._insert_message(x,'Application path not found',"Assistant")
        else:
            t2s('Launching: ' + app)
            obj.launch_any_app(path_of_app=path)
            integrate.ChatApplication._insert_message(x,'Launching: ' + app,"Assistant")

    elif re.search('how are you', res):
        integrate.ChatApplication._insert_message(x,res,"You")
        li = ['good', 'fine', 'great']
        response = random.choice(li)
        t2s(f"I am {response}")
        integrate.ChatApplication._insert_message(x,f"I am {response}","Assistant")

    elif re.search('hello|hi', res):
        integrate.ChatApplication._insert_message(x,res,"You")
        t2s('Hello, how was your day ?')
        integrate.ChatApplication._insert_message(x,'Hello, how was your day ?',"Assistant")

    elif re.search('your name|who are you', res):
        integrate.ChatApplication._insert_message(x,res,"You")
        t2s("I am your personal assistant")
        integrate.ChatApplication._insert_message(x,"I am your personal assistant","Assistant")

    elif re.search('what can you do', res):
        li_commands = {
            "open websites": "Example: 'open youtube.com",
            "time": "Example: 'what time it is?'",
            "date": "Example: 'what date it is?'",
            "launch applications": "Example: 'launch chrome'",
            "tell me": "Example: 'tell me about India'",
            "weather": "Example: 'what weather/temperature in Mumbai?'",
            "news": "Example: 'news for today' ",
        }
        ans = """I can do lots of things, for example you can ask me time, date, weather in your city,
        I can open websites for you, launch application and more. See the list of commands-"""
        integrate.ChatApplication._insert_message(x,res,"You")
        t2s(ans)
        integrate.ChatApplication._insert_message(x,ans,"Assistant")
        for item in li_commands:
            integrate.ChatApplication._insert_message(x,item,"Assistant")

    else:
        if(sent!=0):
            integrate.ChatApplication._insert_message(x,res,"You")
            t2s("alright")
            integrate.ChatApplication._insert_message(x,"alright","Assistant")
        else:
            integrate.ChatApplication._insert_message(x,res,"You")
            t2s("Sorry, did not catch that")
            integrate.ChatApplication._insert_message(x,"Sorry, did not catch that","Assistant") 