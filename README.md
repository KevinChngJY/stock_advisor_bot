
---

## SECTION 1 : PROJECT TITLE
## Stock Advisor Bot

(Still in development)

---

## SECTION 2 : SYSTEM ARCHITECTURE 
## DEPLOY IN LOCAL HOST

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/architecture1.png" width="655" height="350"
     style="float: left; margin-right: 0px;" />
     
## DEPLOY TO SERVER (DIGITAL OCEAN)

## DEPLOY TO CONTAINER

---
## SECTION 3 : EXECUTIVE SUMMARY / PAPER ABSTRACT


---
## SECTION 4 : PROJECT - MILESTONES

| Milestones |  Duration | Remarks |
| :------------ | :-----------------------|:----------------|
| 1.0 RASA |  |  |
| 1.1 RASA in local host|  |  |
| 1.2 RASA + Ngrok + Webhook connect to telegram Chatbot |  |  |
| 1.3 RASA X |  |  |
| 2.0 Content/Response for Chatbot (IPA) |  |  |
| 2.1 Stock Price |  |  |
| 2.2 Sentiment Analysis |  |  |
| 3.0 Integration |  |  |
| 3.1 Setting up Django| | |
| 3.2 Authentication Login In | | |
| 3.3 Database (Django) |  |  |
| 3.4 RASA + Django + Celery + Database | | |
| 4.0 Deployment |  |  |
| 4.1 Deploy in Local Host |  |  |
| 4.2 Deploy to Server (Digital Ocean) |  |  |
| 4.3 Deploy to Container |  |  |


---
## SECTION 5 : Milestone 1 RASA

### What is RASA?

Rasa is an open source machine learning framework for automated text and voice-based conversations. Understand messages, hold conversations, and connect to messaging channels and APIs.

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/rasa.jpeg" width="455" height="250"
     style="float: left; margin-right: 0px;" />
     
Besides RASA, you may consider the following AI chatbot frameworks:

| AI Chatbot |  Programming Languague | NLP Support |
| :------------ | :-----------------------|:----------------|
| [1.0 Microsoft Bot Framework](https://dev.botframework.com/) | NodeJS,C# | No |
| [2.0 RASA](https://rasa.com/) | Python |  Yes |
| [3.0 Wit AI](https://wit.ai/) | Python,Ruby | Yes |
| [4.0 Dialogflow](https://cloud.google.com/dialogflow) | NodeJS | Yes |
| [5.0 IBM Watson](https://www.ibm.com/watson) | Java,C++ | Yes |
| [6.0 Amazon Lex](https://aws.amazon.com/lex/) | Java,.Net,Ruby | Yes |
| [7.0 Pandorabots](https://home.pandorabots.com/home.html) | Java,Ruby,Go,PHP,Python,NodeJS | Yes |
| [8.0 Botpress](https://botpress.com/) | Javascript | Yes |
| [9.0 Botkit](https://botkit.ai/) | NodeJS | No |
| [10.0 ChatterBot](https://chatterbot.readthedocs.io/en/stable/) | NodeJS,Python | Yes |

for detail, you may refer to https://www.spaceo.ca/top-ai-chatbot-frameworks/#link1-3

### Milestone 1.1 Deploy Rasa in Local Host

Document below guide you how to start off RASA : <br>
https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Section5_RASA.md

### Milestone 1.2 RASA + Ngrok + Webhook connect to telegram Chatbot 

Document below guide you how to integrate RASA +  Ngrok + Telegram Chatbot
https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Section5_RASA_NGROK_Telegram.md

### Milestone 1.3 RASA X [Optional]

What is RASA X?
Rasa X is a tool for Conversation-Driven Development (CDD), the process of listening to your users and using those insights to improve your AI assistant.

Documentation : https://rasa.com/docs/rasa-x/

---
## SECTION 6 : Content/Response for Chatbot (IPA)

### Milestone 2.1 Stock Information

Components of Architecture:

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/ComponentsArchitecture1.PNG" width="755" height="350"
     style="float: left; margin-right: 0px;" />
     
Data Structure:<br>
(1) Used for Stock Tick Verification :
| Stock |  Stock Tick |
| :------------ | :-----------------------|
| APPL | AAPL |  |
| Apple | AAPL |  |
| MSFT | MSFT |
| Microsoft Corporation | MSFT |
| Microsoft | MSFT |

 if you key in non stock tick name, the stock tick verification will use your stock name to extract the stock tick name from database and proceed process with stock tick name.<br>

(2) Used for Return Expected Information to User :
| User ID |  Current Price | Price Change | Price Change Percentage | Trading View Link |
| :------------ | :---------|:-----------|:--------|:-------|
| 12221 | 1 | 1 | 0 | 1 |
| 23123 | 1 | 1 | 0 | 0 |

"1" is the feature expected by User, "0" is the feature not expected by user

Above is illustrating the databse, not the full list. The full list of features as follows:
**Price/Volume**
1) Current Price
2) Price Change
3) Price Change Percentage
4) Current Volume
5) Previous Close Price
6) Open Price
7) Get 10 Days Average Volume
8) Get 3 Months Average Daily Volume
9) Get Daily Low Volume
10) Daily High
11) Yearly High
12) Yearly Low
13) Trading View Link <br>
**Fundamental**
14) PE Ratio
15) Market Cap <br>
**Technical Aalysis : Oscillators**
5) Accumulation/disctributor
6) chaikin Money Flow
7) Moving Average Convergennce/Divergence
8) Stochastic Oscillator
11) Percentage Price Oscillator
12) Percentage Volume Oscillator
13) Rate of Change <br>
**Technical Analysis : Stoachastics**
14) Williams %R <br>
**Technical Analysis : Indexes**
15) Negative Volume Index
17) Relative Strength Index (RSI) -14 days
18) Relative Strength Index (RSI) - 28 days <br>
**Technical Analysis : Indicators**
23) On balanced volume
25) Volume-Price Trend
28) Volume Weighted Average Price
30) 50 Days Moving Average
31) 200 Days Moving Average

User can raise to admin for his expected stock information.

Script for Acquire Stock Information from yahoo finance or other financial platform : <br>
https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Milestone2/milestone2_1_Stock%20Information.ipynb

### Milestone 2.2 Sentiment Analysis


### Milestone 2.3 Monitoring Annoucements

Components of Architecture:

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/Architecture2.PNG" width="755" height="350"
     style="float: left; margin-right: 0px;" />
     
Web Crawling Script for Bursa :<br>
Required Packages : urllib,pandas,beautifulsoup,solenium,PhantomJS,requests<br>
[you might need to figure out how to install PhantomJS yourself, it used to deal with JS WebCrawling]<br>
https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Milestone2/milestone2_3_Monitoring_Announcements.ipynb

For this project, it is only applicable for Bursa as we don't develop script to "web-crawl" announcements from other stock exchange. <br>
However, as it is "hobby project", it is okay to do "web-crawling" to illustrate the concept. For real project, you are hughly recommend to purchase api from stock exchange platform.

### Milestone 2.4 Portfolio Optimization and Asset Allocation

Components of Architecture:

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/Architect3.PNG" width="755" height="350"
     style="float: left; margin-right: 0px;" />
 
Script for Portfolio Optimization and Asset Allocation :<br>
https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Milestone2/milestone2_4_Portfolio_analysis.ipynb <br>
We will use image hosting(imgur) as Rasa only can send link(not able to send image) to telegram chatbot.

### Milestone 2.5 Stock Price Forecasting

In time series forecasting, there are couple of techniques you may consider : <br>
Traditional Approaches : <br>
1) Autoregression (AR) <br>
2) Moving Average <br>
3) Autoregressive Moving Average <br>
4) Autoregressive Integrated Moving Average (ARIMA) <br>
5) Seasonal Autoregressive Integrated Moving-Average (SARIMA) <br>
6) Seasonal Autoregressive Integrated Moving Average with Exogenous Regressors (SARIMAX) <br>
8) Regression Model with ARIMA Error <br>
9) Vector Autoregression (VAR) <br>
10) GARCH Model <br>
11) Glostan, Jagannathan and Runkle GARCH Model <br>
you may refer to MATLAB examples in the following link for you to understand how undermentioned models workout :<br>
https://www.mathworks.com/matlabcentral/fileexchange/74211-11-classical-time-series-forecasting-methods-in-matlab

For latest trend, Data Scientist started to explore AI techniques (ML,DL-LSTM,RCNN) in time series forecasting.
However, for this project, we only use ARIMA for this milestone.

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/architecture5.png" width="755" height="350"
     style="float: left; margin-right: 0px;" />
     
Script : https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Milestone2/milestone2_5_Stock_price_time_series_forecasting.ipynb

### Milestone 2.6 Reinforcement Learning for Trading Strategies

---
## SECTION 7 : Integration

### Milestone 3.1 Setting up Django

Reference 1 : https://pythonistaplanet.com/how-to-create-a-django-project-in-anaconda-very-easily/ <br>
Reference 2 : https://www.jcchouinard.com/get-started-with-django/ <br>

You may refer to the 2 references above to learn how to set up django in local PC.<br>
For this project, it did the following actions:<br>

(1) 

### Milestone 3.2 Authentication Login

For production system, it is recommended to use Django in-built Authentication system which can help you manage the session accross the request:
https://www.google.com/search?client=safari&rls=en&q=didjango+authentication&ie=UTF-8&oe=UTF-8

Therefore, in case that you wanted to develop your chatbot further to website or etc, I believe it has additional advantage.

For now, the main purpose of django is providing us the database interface to manage the sqlite. 
[Django is a comprehensive web framework, you can explore yourself to figure additional functions added to your system]

In this milestone, we will go through the following steps:
1) Create database in the models.py (User login Database)
2) Update database using Django Admin Portal
3) Update Rasa for Authentication process:

### Milestone 3.3 Database Django

Setting User list :


Setting Stock Tick Validation Database (Bursa) :


Setting Stock for Annoucement Monitoring : 

---
## SECTION 8 : Deployment


