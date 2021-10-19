from celery import task 
from celery import shared_task
import numpy as np
import pandas as pd
import nltk
import praw
import os
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from .models import sentimentanalysistop10, option3_stock_monitoring,userdatabase
import urllib.request

# Web Scraping for Financial Price
from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.PhantomJS()
import requests
import time

# Time Management
from datetime import datetime, timedelta, date

# We can have either registered task 
@task(name='sentiment') 
def update_sentiment_analysis():
     import time
     # US ticker stocks list is in the same path
     stocks = pd.read_csv('tickers.csv')
     # Last sale column is an object, let's convert to float
     stocks['Last Sale'] = stocks['Last Sale'].str.replace('$','')
     stocks['Last Sale'] = pd.to_numeric(stocks['Last Sale'],downcast='float')
     type(stocks['Last Sale'][0])
     # filter out stocks > usd3 and usd100 million cap
     price_filter = stocks['Last Sale'] >= 3.00
     cap_filter = stocks['Market Cap'] >= 100000000

     # make set of symbols
     stocks = set(stocks[(price_filter) & (cap_filter)]['Symbol'])

     # Includes common words and words used on wsb that are also stock names
     blacklist = {'I', 'ELON', 'WSB', 'THE', 'A', 'ROPE', 'YOLO', 'TOS', 'CEO', 'DD', 'IT', 'OPEN', 'ATH', 'PM', 'IRS', 'FOR','DEC', 'BE', 'IMO', 'ALL', 'RH', 'EV', 'TOS', 'CFO', 'CTO', 'DD', 'BTFD', 'WSB', 'OK', 'PDT', 'RH', 'KYS', 'FD', 'TYS', 'US', 'USA', 'IT', 'ATH', 'RIP', 'BMW', 'GDP', 'OTM', 'ATM', 'ITM', 'IMO', 'LOL', 'AM', 'BE', 'PR', 'PRAY', 'PT', 'FBI', 'SEC', 'GOD', 'NOT', 'POS', 'FOMO', 'TL;DR', 'EDIT', 'STILL', 'WTF', 'RAW', 'PM', 'LMAO', 'LMFAO', 'ROFL', 'EZ', 'RED', 'BEZOS', 'TICK', 'IS', 'PM', 'LPT', 'GOAT', 'FL', 'CA', 'IL', 'MACD', 'HQ', 'OP', 'PS', 'AH', 'TL', 'JAN', 'FEB', 'JUL', 'AUG', 'SEP', 'SEPT', 'OCT', 'NOV', 'FDA', 'IV', 'ER', 'IPO', 'MILF', 'BUT', 'SSN', 'FIFA', 'USD', 'CPU', 'AT', 'GG', 'Mar'}
     # Adding wsb/reddit flavor to vader to improve sentiment analysis, score: 4.0 to -4.0
     new_words = {
    'citron': -4.0,  
    'hidenburg': -4.0,        
    'moon': 4.0,
    'highs': 2.0,
    'mooning': 4.0,
    'long': 2.0,
    'short': -2.0,
    'call': 4.0,
    'calls': 4.0,    
    'put': -4.0,
    'puts': -4.0,    
    'break': 2.0,
    'tendie': 2.0,
     'tendies': 2.0,
     'town': 2.0,     
     'overvalued': -3.0,
     'undervalued': 3.0,
     'buy': 4.0,
     'sell': -4.0,
     'gone': -1.0,
     'gtfo': -1.7,
     'paper': -1.7,
     'bullish': 3.7,
     'bearish': -3.7,
     'bagholder': -1.7,
     'stonk': 1.9,
     'green': 1.9,
     'money': 1.2,
     'print': 2.2,
     'rocket': 2.2,
     'bull': 2.9,
     'bear': -2.9,
     'pumping': -1.0,
     'sus': -3.0,
     'offering': -2.3,
     'rip': -4.0,
     'downgrade': -3.0,
     'upgrade': 3.0,     
     'maintain': 1.0,          
     'pump': 1.9,
     'hot': 1.5,
     'drop': -2.5,
     'rebound': 1.5,  
     'crack': 2.5,}

     # Magic happens here ...
     print("Running sentiment analysis, this may take a few minutes...\n")
     # Instantiate praw object
     start_time = time.time()
     reddit = praw.Reddit(user_agent="Comment Extraction", client_id = "QktIf3FZ10C5jg" , client_secret= "52XN7-d-s7tBO8Wld9mPQ19PMaV8HA")

     # Set program parameters
     subs = ['wallstreetbets', 'stocks', 'investing', 'stockmarket']     # sub-reddit to search
     post_flairs = {'Daily Discussion', 'Weekend Discussion', 'Discussion'}    # posts flairs to search || None flair is automatically considered
     goodAuth = {'AutoModerator'}   # authors whom comments are allowed more than once
     uniqueCmt = True                # allow one comment per author per symbol
     ignoreAuthP = {'example'}       # authors to ignore for posts 
     ignoreAuthC = {'example'}       # authors to ignore for comment
     upvoteRatio = 0.70         # upvote ratio for post to be considered, 0.70 = 70%
     ups = 20       # define # of upvotes, post is considered if upvotes exceed this #
     limit = 10      # define the limit, comments 'replace more' limit
     upvotes = 2     # define # of upvotes, comment is considered if upvotes exceed this #
     picks = 10     # define # of picks here, prints as "Top ## picks are:"
     picks_ayz = 10   # define # of picks for sentiment analysis

     # Define variables
     posts, count, c_analyzed, tickers, titles, a_comments = 0, 0, 0, {}, [], {}
     cmt_auth = {}

     # start web-crawling and do the sentiment analysis
     # start web-crawling and do the sentiment analysis
     for sub in subs:
          subreddit = reddit.subreddit(sub)
          hot_python = subreddit.hot()
          # Extracting comments, symbols from subreddit
          for submission in hot_python:
               flair = submission.link_flair_text
               author = submission.author #name
        
               #checking: post upvote ratio # of upvotes, post filter, and author
               if submission.upvote_ratio >= upvoteRatio and submission.ups > ups and (flair in post_flairs or flair is None) and author not in ignoreAuthP:
                      submission.comment_sort = 'new'
                      comments = submission.comments
                      titles.append(submission.title)
                      posts += 1
                      submission.comments.replace_more(limit = limit)
                      for comment in comments:
                          # try except for deleted account?
                          try:
                              auth = comment.author.name
                          except:
                              pass
                          c_analyzed += 1

                          # checking: comment upvotes and author
                          if comment.score > upvotes and auth not in ignoreAuthC:
                              split = comment.body.split(' ')
                              for word in split:
                                  word = word.replace("$", "")
                                  # upper = ticker, length of ticker <= 5, excluded words
                                  if word.isupper() and len(word) <= 5 and word not in blacklist and word in stocks:
                                      
                                      # unique comments, try/except for key errors
                                      if uniqueCmt and auth not in goodAuth:
                                          try:
                                              if auth in cmt_auth[word]:
                                                  break
                                          except:
                                              pass
                                      
                                      # counting tickers
                                      if word in tickers:
                                          tickers[word] += 1
                                          a_comments[word].append(comment.body)
                                          cmt_auth[word].append(auth)
                                          count += 1
                                      else:
                                          tickers[word] = 1
                                          cmt_auth[word] = [auth]
                                          a_comments[word] = [comment.body]
                                          count += 1

     # sorts the dictionary
     symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True))
     top_picks = list(symbols.keys())[0:picks]
     time = (time.time() - start_time)

     # print top picks
     msg="It took {t:.2f} seconds to analyze {c} comments in {p} posts in {s} subreddits.\n".format(t=time,
                                                                                                c=c_analyzed,
                                                                                                p=posts,
                                                                                                s=len(subs))
     print(msg)
     obj=sentimentanalysistop10.objects.get(categories="other")
     obj.top10 = msg
     obj.save()
     print("Posts analyzed saved in titles")
     # for i in titles: print(i) # prints the title of the posts analyzed
     print(f"\n{picks} most mentioned picks: ")
     times = []
     top = []
     for i in top_picks:
          #print(f"{i}: {symbols[i]}")
          times.append(symbols[i])
          top.append(f"{i}: {symbols[i]}")
          #print(' '.join(map(str, top)))
     top_10 = "{},{},{},{},{},{},{},{},{},{}".format(top[0],top[1],top[2],top[3],top[4],top[5],top[6],top[7],top[8],top[9])
     print(top_10)
     obj=sentimentanalysistop10.objects.get(categories="Most_Mentioned")
     obj.top10 = top_10
     obj.save()
     
     # Applying sentiment analysis
     scores, s = {}, {}
     vader = SentimentIntensityAnalyzer()
     # adding custom words from data.py
     vader.lexicon.update(new_words)
     picks_sentiment = list(symbols.keys())[0: picks_ayz]
     for symbol in picks_sentiment:
          stock_comments = a_comments[symbol]
          for cmnt in stock_comments:
               score = vader.polarity_scores(cmnt)
               if symbol in s:
                    s[symbol][cmnt] = score
               else:
                    s[symbol] = {cmnt: score}
               if symbol in scores:
                    for key, _ in score.items():
                         scores[symbol][key] += score[key]
               else:
                    scores[symbol] = score

          # calculating averages
          for key in score:
               scores[symbol][key] = scores[symbol][key] / symbols[symbol]
               scores[symbol][key] = "{pol:.3f}".format(pol=scores[symbol][key])

     # Printing sentiment analysis
     print(f"\nSentiment analysis of top {picks_ayz} picks:")
     df = pd.DataFrame(scores)
     df.index = ['Bearish', 'Neutral', 'Bullish', 'Total_Compound']
     df = df.T
     print(df)
     msg=""
     for i in range(0,10):
          msg = msg + "{}:{} {} {} {},".format(df.index[i],df.iloc[i].Bearish,df.iloc[i].Neutral, df.iloc[i].Bullish,df.iloc[i].Total_Compound)
     obj=sentimentanalysistop10.objects.get(categories="sentime_result_top_10_mentioned")
     msg = msg[:-1]
     obj.top10 = msg
     obj.save()

#@shared_task
@task(name='announcement') 
def send_notifiction_announcement():
     stock_list_from_database = option3_stock_monitoring.objects.filter().values_list('company_official')
     list_of_selected_stock = [k[0].upper() for k in list(stock_list_from_database)] 
     #list_of_selected_stock = ["GENTING MALAYSIA BERHAD", "M3 TECHNOLOGIES (ASIA) BERHAD"]
     [Company,Title,Link]=get_information_stock(list_of_selected_stock)
     msg = ""
     for ci,ti,li in zip(Company,Title,Link):
          msg = msg + "{} : {} ,\nLink : {} \n\n".format(ci,ti,li)

     # send telegram to user
     for ci,ti,li in zip(Company,Title,Link):
          obj=option3_stock_monitoring.objects.filter(company_official=ci)
          for user in obj:
               user_id = userdatabase.objects.get(username=user.username)
               telegram_id = user_id.telegram_id
               msg = "**Anouncement**\n"
               msg = msg + "Company : {}\n".format(ci)
               msg = msg + "Title : {}\n".format(ti)
               msg = msg + "Link : {}".format(li)
               url = "https://api.telegram.org/bot1913586416:AAGMxSxcu-FwmFp6ZGRHHjBIvK8f8O8YWjs/sendMessage?chat_id={}&text={}".format(telegram_id,msg)
               x = requests.post(url)


def get_information_stock(list_stock):
    import time
    temp_build=1
    Company = []
    Title = []
    Link = []
    today_check=True
    while(today_check):
        website = "https://www.bursamalaysia.com/market_information/announcements/company_announcement?page={}".format(temp_build)
        print(website)
        driver.get(website)
        p_element = driver.find_element_by_id(id_='table-announcements')
        w=p_element.get_attribute('outerHTML')
        BloomSoup = BeautifulSoup(w)
        contents = BloomSoup.find_all('tr')
        for p in range(1,len(contents)):
            mydivs = contents[p].find_all("div", {"class": "d-lg-inline-block d-none"})
            list_a = contents[p].find_all('a')
            check_company=list_a[0].text.replace("\n","")
            today = date.today().strftime('%d %b %Y')
            if today not in mydivs[0].text:
                today_check=False
            if check_company in list_stock:
                print(check_company)
                Company.append(check_company)
                Title.append(list_a[1].text.replace("\n",""))
                Link.append("https://www.bursamalaysia.com"+list_a[1]['href']) 
        time.sleep(1)                      
        #Update page number
        temp_build = temp_build +1
    return Company,Title,Link