from django.shortcuts import render
from django.http import HttpResponse
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener 
import time
import json
import asyncio
import websockets
from tornado import ioloop
from queue import Queue
queue = Queue()
# authentication

def authTwitter():
    try:
        # Set these these keys to environmental variable 
        consumer_key = "HhZg3kDcPxQiX7pUCg95lzIhi"
        consumer_secret ="RwPrR82cLy38wMqeGG6ozzKEizqVjMbtDzDatWAbCEJkkVF33m"
        access_token = "1319535856613425152-F2ILps9CmM57JBZsmMKfvjHU5bKU0S"
        access_token_secret = "wVCv7om5NJUchoLZmfCwzubERHAdKvrJFvhDx5Gh7NhFC"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth
    except KeyError:
        print("Keyerror")



auth = authTwitter()  
api = tweepy.API(auth)                

class MyStreamListener(tweepy.StreamListener):    
    def on_status(self, status):       
        queue.put(status.text)
    def on_error(self, status_code):
        if status_code == 420:            
            return False
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = auth, listener=myStreamListener)

def startStream(*keyword):
    k = keyword[0]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)     
    print(k)
    if len(keyword) <=1 :
        myStream.filter(track=[k])
    else:        
        myStream.filter(follow=[k])
import asyncio
import websockets
import json
async def hello():    
    uri = "ws://localhost:8000/ws/fetchTweet/add/"
    async with websockets.connect(uri) as websocket:
        while True:
            if(not queue.empty()):
                message= queue.get()
                # print(message)
                await websocket.send(json.dumps({
                    'message': message
                }))
                # print(f"> {message}")
                greeting = await websocket.recv()
                # print(f"< {greeting}")
                       

def startServer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(hello())    
from threading import Thread


t2 = Thread(target = startServer)
t2.start()

def keyWordTweets(request):
    if request.method == 'GET':        
        return render(request, 'fetchTweet/keyword.html')
    if request.method == 'POST':
        keyword = request.POST.get("keyword")
        print(keyword)
        t1 = Thread(target = startStream ,args=[keyword]) 
        t1.start()    
        return render(request, 'fetchTweet/tweets.html')
def userTweets(request):
    if request.method == 'GET':         
        return render(request, 'fetchTweet/user.html')
    if request.method == 'POST':
        username = request.POST.get("username")
        t1 = Thread(target = startStream ,args=[username]) 
        t1.start()      
        numbmsg = int(request.POST.get("numbmsg"))                      
        tweets = []
        for tweet in tweepy.Cursor(api.search, q=username).items(numbmsg):
            tweets.append(tweet.text)     
        context = {
            "username" : username,
            "numbmsg" : numbmsg,
            "tweets" : tweets             
        }
        return render(request, 'fetchTweet/tweets.html',context)

def home(request):
    return render(request, 'fetchTweet/home.html')