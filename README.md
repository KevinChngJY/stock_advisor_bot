## SECTION 1 : PROJECT TITLE
## Finance Bot

The project envisions to develop a TELEGRAM STOCK ADVISOR BOT to (a) empower people with useful stock information and (2) bring convenience and time savings to people.

The BOT will be equipped with the following functions and features :

Features of Bot :
| Modules |  Features | 
| :------------ | :-----------------------|
| 1.0 Stock Information | Get Stock Price, Fundamental & Technical Indicators |  
| 2.0 Sentiment Analysis| Return market sentiment outcome |  
| 3.0 Monitoring Announcement | Market Announcement Notification according to user’s stock watchlist |  
| 4.0 Portfolio Optimization and Asset Allocation | Correlation, Risk Assessment, Portfolio Optimization and Asset Allocation, etc|
| 5.0 Time Series Forecasting | Classical Time Series Forecasting Technique, Machine Learning and Deep Learning |  
| 6.0 Reinforcement Learning & Evolving Learning| Trading strategies advise according to result of RL policy and traditional benchmark (RSI and etc) 

The TELEGRAM BOT is designed with the end-user in mind, and the dialogue/workflow is designed to be as user friendly and iniuitive as possible.<br>
Below is the menu of the bot:<br>

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/bot_menu.PNG" width="455" height="350"
     style="float: left; margin-right: 0px;" />
     
Demonstration of the system (Video) - Marketing:

Demonstration of the system (Video) - High Level Architecture Explaination:


the following section 2 - 5 explains the steps how we build the system.
if you are looking to run the system, you may direct jump to section 7 : Guide to run the system locally.

---

## SECTION 2 : SYSTEM ARCHITECTURE 
## DEPLOY IN LOCAL HOST

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/architecture1.PNG" width="655" height="350"
     style="float: left; margin-right: 0px;" />
     
API Gateway of system is using ngrok (Between telegram and Rasa OpenSource Server/Django)

In this project, besides telegram chat platform, if user selects option 6 : Reinforcement Learning & Evolving Learning, it would navigate user to website. (Therefore, we need 2 ports (forwarding to external) through ngrok. In ngrok, for 2 port forwarding from local, it has to pay USD 10 monthly subscription (as per 31 Oct 2021).

---
## SECTION 3 : PROJECT - MILESTONES

| Milestones |  Duration (th Week) | Remarks |
| :------------ | :-----------------------|:----------------|
| 1.0 RASA | 0-1 |  |
| 1.1 RASA in local host| 0-1 |  |
| 1.2 RASA + Ngrok + Webhook connect to telegram Chatbot | 0-1 |  |
| 1.3 RASA X |  |  |
| 2.0 Content/Response for Chatbot (IPA) | 1-7 |  |
| 2.1 Stock Price | 1-5 |  |
| 2.2 Sentiment Analysis | 1-5 |  |
| 2.3 Monitoring Announcement | 1-5 |  |
| 2.4 Portfolio Optimization and Asset Allocation | 1-5 |  |
| 2.5 Time Series Forecasting | 1-5 |  |
| 2.6 Reinforcement Learning | 5-7 |  |
| 3.0 Integration | 7-10 |  |
| 3.1 Setting up Django| 7-8 | |
| 3.2 Authentication Login In | 7-8 | |
| 3.3 Database (Django) - Structures & Data WebCrawling to update Database |  8-9 |  |
| 3.4 RASA + Django + Celery + Database | 9-10 | |
| 4.0 Deployment |  |  |
| 4.1 Deploy in Local Host | 10 |  |
| 4.2 Deploy to Server (Digital Ocean) | 11 |  |
| 4.3 Deploy to Container | 12 |  |
| 5.0 User-Interface & Report | 12 |  |

The project take estimated 12 weeks (3months) to complete, it does not include bug-fixing and UAT process.

---
## SECTION 4 : Milestone 1 RASA

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
## SECTION 5 : Content/Response for Chatbot (IPA)

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
Thee are various well known NLB libraries in Python : <br>

**Rule-based methods:** <br>
TextBlob: Simple rule-based API for sentiment analysis <br>
VADER: Parsimonious rule-based model for sentiment analysis of social media text. <br>
**Feature-based methods:**
Logistic Regression: Generalized linear model in Scikit-learn.
Support Vector Machine (SVM): Linear model in Scikit-learn with a stochastic gradient descent (SGD) optimizer for gradient loss.
**Embedding-based methods:**
FastText: An NLP library that uses highly efficient CPU-based representations of word embeddings for classification tasks.
Flair: A PyTorch-based framework for NLP tasks such as sequence tagging and classification.

For this section, we use VADER approach to perform sentiment analysis for the contents in Reddit. <br>
To know Vader further, you may refer to the following link : https://www.geeksforgeeks.org/python-sentiment-analysis-using-vader/ <br>

With Reddit Python API package, we search for 4 topics which are 'wallstreetbets', 'stocks', 'investing', 'stockmarket’. From this 4 topics, it computes the top 10 most mentioned US stocks and subsequently use lexicon-based approach (VADER) to perform the sentiment analysis of the top 10 most mentioned US stocks from the comments in the reddit.

Script : https://github.com/KevinChngJY/stock_advisor_bot/tree/main/Milestone2/Milestone2_2_Sentiment_Analysis

### Milestone 2.3 Monitoring Annoucements

Components of Architecture:

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/Architecture2.PNG" width="755" height="350"
     style="float: left; margin-right: 0px;" />
     
Web Crawling Script for Bursa :<br>
Required Packages : urllib,pandas,beautifulsoup,solenium,PhantomJS,requests<br>
[you might need to figure out how to install PhantomJS yourself, it used to deal with JS WebCrawling]<br>
https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Milestone2/milestone2_3_Monitoring_Announcements.ipynb

For this project, it is only applicable for Bursa as we don't do "web-crawling" for announcements in other stock exchange. <br>
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

### Milestone 2.6 Reinforcement Learning and Evolving Learning for Trading Strategies

In this milestone, there are 2 algorihtms (RL and GA) to optimize the trading strategies:

**What is Reinforcement Learning?**
Reinforcement learning is another type of machine learning besides supervised and unsupervised learning. This is an agent-based learning system where the agent takes actions in an environment where the goal is to maximize the record. Reinforcement learning does not require the usage of labeled data like supervised learning.

Reinforcement learning works very well with rich historical data. It makes use of the value function and calculates it on the basis of the policy that is decided for that action.

**Define the Reinforcement Learning Environment**<br>
MDP for Stock Price Prediction: 

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/MDP_Reinforcement_Learning.png" width="455" height="200"
     style="float: left; margin-right: 0px;" />

Agent – An Agent A that works in Environment E <br>
Action – Buy/Sell/Hold<br>
States – Data values<br>
Rewards – Profit / Loss<br>

**Script - Reinforcement Learning**<br>
In this milestone, we use deep Q-Learning algorithm to train the policy for trading strategy.<br>
Script for Reinforcement Learning : https://github.com/KevinChngJY/stock_advisor_bot/tree/main/Milestone2/Milestone2_6_Reinforcement_Learning_Trading_Strategy

**What is Genetic Algorithm?**<br>
In computer science and operations research, a genetic algorithm (GA) is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms (EA). Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on biologically inspired operators such as mutation, crossover and selection.

In layman term, it is a type of global optimization algorihm to optimize the parameters in your complex mathematical equations/objective function

**Script - Evolving Learning**<br>
In this script, we don't include mutation in the GA algorithm.<br>
Script for RSI Indicators : https://github.com/KevinChngJY/stock_advisor_bot/tree/main/Milestone2/Milestone2_6_Evolving_Learning-Trading_Algorithm

---
## SECTION 6 : Integration

### Milestone 3.1 Setting up Django

Reference 1 : https://pythonistaplanet.com/how-to-create-a-django-project-in-anaconda-very-easily/ <br>
Reference 2 : https://www.jcchouinard.com/get-started-with-django/ <br>

You may refer to the 2 references above to learn how to set up django in local PC.<br>

### Milestone 3.2 Authentication Login

For production system, it is recommended to use Django in-built Authentication system which can help you manage the session accross the request:
https://www.google.com/search?client=safari&rls=en&q=didjango+authentication&ie=UTF-8&oe=UTF-8

Therefore, in case that you wanted to develop your chatbot further to website or etc, I believe it has additional advantage.

For now, the main purpose of django is providing us the database interface to manage the sqlite. 
[Django is a comprehensive web framework, you can explore yourself to figure additional functions added to your system]

In this milestone, we will go through the following steps:
1) Create database in the models.py (User login Database):

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/userdatabase.png" width="455" height="150"
     style="float: left; margin-right: 0px;" />
     
2) Update database (User List) using Django Admin Portal

Once you run django server locally "python manage.py runserver", then open the database portal : http://127.0.0.1:8000/admin. <br>
Log in your username and password, then you would see the user list. <br>

You could add your user to the userlist, you may notice that it requires you to add telegramid when you cratea a new user.<br>
Telegramid is required for the features 3 - 2.3 Monitoring Annoucements. Once the user has added stock to the stock monitoring list, if there is any announcement for this stock, the celery system would send the announcement to the registered telegramid.

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/userdatabase_django.png" width="455" height="200"
     style="float: left; margin-right: 0px;" />
     
**How do you get the telegramid?**<br>
https://www.wikihow.com/Know-Chat-ID-on-Telegram-on-Android#:~:text=Locate%20%22Chat.%22%20It's%20about,Last%20Name%2C%20and%20your%20Username.&text=Note%20the%20number%20next%20to,is%20your%20personal%20Chat%20ID.

4) Update Rasa for Authentication process

We will use RASA Actions Server to validate the userlogin with the userlist in the database. Below is the code in RASA Action Server:

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/login_validate.png" width="455" height="600"
     style="float: left; margin-right: 0px;" />
     
### Milestone 3.3 Database Django

There are 5 table in the database for this project : 

**User list :** <br>
<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/userlist_database.png" width="455" height="150"
     style="float: left; margin-right: 0px;" />
     
**Bursa Stock list:** <br>
<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/bursalist_database.png" width="455" height="150"
     style="float: left; margin-right: 0px;" />
     
**Option1_selection :** <br>
<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/option1_indicators_database.png" width="455" height="500"
     style="float: left; margin-right: 0px;" />
     
**Option3_stock_monitorings :** <br>
<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/option3_stock_monitoring_database.png" width="455" height="160"
     style="float: left; margin-right: 0px;" />
     
**sentimentanalysistop10 :** <br>
<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/sentiment_analysis_10_list.png" width="455" height="150"
     style="float: left; margin-right: 0px;" />

### Milestone 3.4 WebApp for Option 2.6 Reinforcement Learning and Evolving Learning for Trading Strategies

### Milestone 3.4 RASA + Django + Celery + Database

---
## SECTION 7 : Run the system in your local machine

### Install Pre-requisites

**Step 1 : Install NGROK in your machine**
https://ngrok.com/

**Step 2 : Install Anaconda**
https://www.anaconda.com/products/individual

**Step 3 : Clone this repository to your system**

**Step 4 : Complete Milestone 1.2 - Setup Telegram FatherBot and webhook to RASA Open Source Server
https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Section5_RASA_NGROK_Telegram.md

Ensure you can get the same result. 

**Step 5 : Install packages for rasa open source server environment**

Open Anaconda Prompt to set up the environmet for rasa open source server

```
conda create -n rasa_server python=3.6
conda activate rasa_server
```

```
pip3 install -U --user pip
```

```
pip3 install rasa[full]
```

**Step 6 : Install packages for rasa action server environment**

In your anaconda prompt, kindly run the following command to set up the environment for rasa action server

```
conda create -n rasa_server_action python=3.6
conda activate rasa_server_action
```

```
pip3 install -U --user pip
pip3 install rasa[full]
```

```
pip install yahoofinancials
pip install pandas-datareader
pip install yfinance
pip install ta
pip install praw
pip install squarify
conda install -c anaconda sqlite
conda install -c trentonoliphant datetime
conda install -c conda-forge ta-lib=0.4.19
conda install numpy
conda install pandas
conda install -c anaconda statsmodels
conda install -c anaconda scikit-learn
conda install -c anaconda nltk
```

**Step 7 : Install packages for Django environment**

In your anaconda prompt, kindly run the following command to set up the environment for Django environment

```
conda create -n django_server python=3.8
conda activate django_server
```

```
conda install -c anaconda django
pip install celery
pip install redis
```

Install Redis & start it up locally at port 6379:
https://redis.io/topics/quickstart

```
conda install -c conda-forge djangorestframework
conda install -c anaconda requests
conda install -c conda-forge keras
conda install -c conda-forge tensorflow
```

you might have error in installing tensorflow in anaconda, it is pretty common, i believe you could found the solution online.

```
pip install python-dateutil
pip install pandas-datareader
pip install tagenalgo
pip install numba
pip install scikit-learn
pip install ta
```


### Run servers

Start Ngrok
```
ngrok http 5005
```

Start Django Server
```
python manage.py runserver
```

Start Celery Scheduler
```
celery -A chatbot worker -B -l INFO
```

Start Rasa Open Source Server
```
rasa run
```

Start Rasa Action Server
```
rasa run actions
```
