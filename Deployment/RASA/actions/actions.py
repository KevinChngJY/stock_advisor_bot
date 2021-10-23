# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from yahoofinancials import YahooFinancials
from pandas_datareader import data
import yfinance as yf
import sqlite3
from datetime import date
from dateutil.relativedelta import relativedelta
from ta.momentum import RSIIndicator, PercentagePriceOscillator, PercentageVolumeOscillator,ROCIndicator,StochasticOscillator
from ta.volume import AccDistIndexIndicator, ChaikinMoneyFlowIndicator, NegativeVolumeIndexIndicator, OnBalanceVolumeIndicator, VolumePriceTrendIndicator, VolumeWeightedAveragePrice
import requests
import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import nltk
import praw
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date

#
class Option11_Price(Action):
#
     def name(self) -> Text:
         return "option1_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         #Get today date
         today = date.today()
         # YYYY-MM-DD
         d1 = today.strftime("%Y-%m-%d")

         #Get company name 
         slot_value = tracker.get_slot('stocktick')
         con = sqlite3.connect("../../Django/db.sqlite3")
         cursor = con.execute("SELECT company_official from rasa_chatbot_bursalist WHERE company_tickname='{}'".format(slot_value))
         row = cursor.fetchone()
         msg = "Today: {}\n\n{} :\n\n**Price-MYR**\n".format(str(d1),row[0])

         #check_customer_requirement
         username = tracker.get_slot("username")
         cursor = con.execute("SELECT * from rasa_chatbot_option1_selection WHERE username='{}'".format(username))
         row = cursor.fetchone()
         con.close()

         #yahho finance
         string_check = "{}.KL".format(slot_value)
         yahoo_financials = YahooFinancials(string_check)

         #Price
         if row[2]:
            ind=yahoo_financials.get_current_price()
            if ind:
                msg = msg + "Current Price: {}\n".format(ind)
         if row[3]:
            current_change = round(yahoo_financials.get_current_change(),2)
            current_change_percent = yahoo_financials.get_current_percent_change()*100
            if current_change and current_change_percent:
                msg = msg + "Changes: {:.2f}({:.2f}%)\n".format(current_change,current_change_percent)
         if row[5]:
            ind=yahoo_financials.get_prev_close_price()
            if ind:
                msg = msg + "Previous Close Price: {:.3f}\n".format(ind)
         if row[6]:
            ind = yahoo_financials.get_open_price()
            if ind:
                msg = msg + "Open Price: {:.3f}\n".format(ind)
         if row[7]:
            ind = yahoo_financials.get_daily_low()
            if ind:
                msg = msg + "Daily Low: {:.3f}\n".format(ind)
         if row[8]:
            ind = yahoo_financials.get_daily_high()
            if ind:
                msg = msg + "Daily High: {:.3f}\n".format(ind)
         if row[9]:
            ind = yahoo_financials.get_yearly_low()
            if ind:
                msg = msg + "Yearly Low: {:.3f}\n".format(ind)
         if row[10]:
            ind = yahoo_financials.get_yearly_high()
            if ind:
                msg = msg + "Yearly High: {:.3f}\n".format(ind)
         if row[11]:
            ind=yahoo_financials.get_50day_moving_avg()
            if ind:
                msg = msg + "50 Days Average: {:.3f}\n".format(ind)
         if row[12]:
            ind=yahoo_financials.get_200day_moving_avg()
            if ind:
                msg = msg + "200 Days Average: {:.3f}\n".format(ind)

         #Volume
         msg = msg + "\n**Volume**\n"
         if row[13]:
            ind=yahoo_financials.get_current_volume()/1000
            if ind:
                msg = msg + "Current Volume: {:.0f}k\n".format(ind)
         if row[14]:
            ind=yahoo_financials.get_ten_day_avg_daily_volume()/1000
            if ind:
                msg = msg + "10 Days Average: {:.0f}k\n".format(ind)
         if row[15]:
            ind=yahoo_financials.get_three_month_avg_daily_volume()/1000
            if ind:
                msg = msg + "3 Months Average: {:.0f}k\n".format(ind)

         #Fundamental
         msg = msg + "\n**Fundamental Indicator**\n"
         if row[16]:
            ind=yahoo_financials.get_market_cap()/1000
            if ind:
                msg = msg + "Market Cap: {:.0f}k\n".format(ind)
         if row[17]:
            ind=yahoo_financials.get_pe_ratio()
            if ind:
                msg = msg + "Market Cap: {:.2f}\n".format(ind)

         #download stock price
         startdate =  date.today() + relativedelta(months=-3)
         df = yf.download(string_check,start=startdate,end=d1)

         #Technical Indicator
         msg = msg + "\n**Technical Indicator**\n"
         if row[18]:
            ind=RSIIndicator(close=df["Close"],window=14,fillna=True)
            if ind:
                msg = msg + "RSI-14: {:.2f}\n".format(ind.rsi()[-1])
         if row[19]:
            ind=RSIIndicator(close=df["Close"],  window= 28, fillna = True)
            if ind:
                msg = msg + "RSI-28: {:.2f}\n".format(ind.rsi()[-1])
         if row[20]:
            ind = PercentagePriceOscillator(close=df["Close"],  window_slow=26,window_fast=12,window_sign=9,fillna = True)
            if ind:
                msg = msg + "Percentage Price Oscillator: {:.2f}\n".format(ind.ppo()[-1])
         if row[21]:
            ind = PercentageVolumeOscillator(volume=df["Volume"],  window_slow=26,window_fast=12,window_sign=9,fillna = True)
            if ind:
                msg = msg + "Percentage Volume Oscillator: {:.2f}\n".format(ind.pvo()[-1])
         if row[22]:
            ind = ROCIndicator(close=df["Close"],  window=12,fillna = True)
            if ind:
                msg = msg + "Rate of Change: {:.2f}\n".format(ind.roc()[-1])
         if row[23]:
            ind = StochasticOscillator(close=df["Close"],  high=df["High"],low=df["Low"],window=14,smooth_window=3,fillna = True)
            if ind:
                msg = msg + "Stochastic Oscvillator: {:.2f}\n".format(ind.stoch()[-1])
         if row[25]:
            ind = AccDistIndexIndicator(close=df["Close"],  high=df["High"],low=df["Low"],volume=df["Volume"],fillna = True)
            if ind:
                msg = msg + "ADI: {:.2f}\n".format(ind.acc_dist_index()[-1])
         if row[26]:
            ind = ChaikinMoneyFlowIndicator(close=df["Close"],  high=df["High"],low=df["Low"],volume=df["Volume"],fillna = True)
            if ind:
                msg = msg + "Chaikin Money FLow: {:.2f}\n".format(ind.chaikin_money_flow()[-1])
         if row[27]:
            ind = NegativeVolumeIndexIndicator(close=df["Close"],volume=df["Volume"],fillna = True)
            if ind:
                msg = msg + "Negative Volume Index: {:.2f}\n".format(ind.negative_volume_index()[-1])
         if row[28]:
            ind = OnBalanceVolumeIndicator(close=df["Close"],volume=df["Volume"],fillna = True)
            if ind:
                msg = msg + "OnBalance Volume: {:.2f}\n".format(ind.on_balance_volume()[-1])
         if row[29]:
            ind = VolumePriceTrendIndicator(close=df["Close"],volume=df["Volume"],fillna = True)
            if ind:
                msg = msg + "Volume Price Trend: {:.2f}\n".format(ind.volume_price_trend()[-1])
         if row[30]:
            ind = VolumeWeightedAveragePrice(close=df["Close"],high=df["High"],low=df["Low"],volume=df["Volume"],window=14,fillna = True)
            if ind:
                msg = msg + "Volume Weighted Average Price: {:.2f}\n".format(ind.volume_weighted_average_price()[-1])

         #Trading View
         tradingviewlink ="https://www.tradingview.com/chart/?symbol={}".format(slot_value)
         msg = msg + "\n Trading View Link : {}".format(tradingviewlink)

         #msg = "{} :\n\n**Price**\nCurrent Price: {}\nChanges: {:.2f}({:.2f}%)\nPrevious Close Price:\nOpen Price:\n\n**Volume**\n\n**Trading Views** :\n{}".format(row[0],current_price,current_change,current_change_percent,tradingviewlink)

         buttons = [{"title": "Back to Menu", "payload": "/start"}]
         dispatcher.utter_message(text=msg,buttons=buttons)

         return [SlotSet("stocktick", None)]

class Option2_1(Action):
#
     def name(self) -> Text:
         return "option2_1_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         authentication = tracker.get_slot('authentication')

         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return []
         else:
            #Get today date
            today = date.today()
            # YYYY-MM-DD
            d1 = today.strftime("%d-%m-%Y")
            #check_customer_watch_list
            msg = "Sentiment Analysis\n\nToday is : {}\n\n".format(d1)
            # Connect to database
            con = sqlite3.connect("../../Django/db.sqlite3")
            cursor = con.execute("SELECT top10 from rasa_chatbot_sentimentanalysistop10 WHERE categories='sentime_result_top_10_mentioned'")
            row1 = cursor.fetchone()
            cursor = con.execute("SELECT top10 from rasa_chatbot_sentimentanalysistop10 WHERE categories='Most_Mentioned'")
            row2 = cursor.fetchone()
            cursor = con.execute("SELECT top10 from rasa_chatbot_sentimentanalysistop10 WHERE categories='other'")
            row3 = cursor.fetchone()
            msg = msg + "This sentiment analysis is scheduled to run at midnight 00:00am everyday to update the latest top10 most mentioned stock pick.{}\n\n".format(row3[0])
            top10_mentioned=row2[0].split(',')
            top10_sentiment=row1[0].split(',')
            msg = msg + "10 most mentioned picks:\n"
            for stock in top10_mentioned:
                msg = msg + "{}\n".format(stock)
            msg = msg + "\nSentiment Analysis of top 10 picks:\n"
            for stock in top10_sentiment:
                index = stock.find(":")
                value_s = stock[index:]
                stockname = stock[:index]
                value_s = value_s.split(' ')
                msg = msg + "*{}*\n".format(stockname)
                msg = msg + "Bearish : {}\n".format(value_s[0])
                msg = msg + "Neutral : {}\n".format(value_s[1])
                msg = msg + "Bullish : {}\n".format(value_s[2])
                msg = msg + "Total Compount : {}\n".format(value_s[3])
            # return result
            buttons = [{"title": "Back to Menu", "payload": "/option2"}]
            dispatcher.utter_message(text=msg,buttons=buttons)
            return []

class Option3_1(Action):
#
     def name(self) -> Text:
         return "option3_1_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         authentication = tracker.get_slot('authentication')

         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return []
         else:
            #check_customer_watch_list
            con = sqlite3.connect("../../Django/db.sqlite3")
            username = tracker.get_slot("username")
            cursor = con.execute("SELECT company_official from rasa_chatbot_option3_stock_monitoring WHERE username='{}'".format(username))
            row = cursor.fetchall()
            con.close()
         
            msg = "Stock Monitoring List\n\n"
            iter_ind=1
            for stock in row:
                msg = msg + "{}. {}\n".format(iter_ind,stock[0])
                iter_ind = iter_ind + 1

            buttons = [{"title": "Back to Menu", "payload": "/option3"}]
            dispatcher.utter_message(text=msg,buttons=buttons)
            return []

class Option3_2(Action):
#
     def name(self) -> Text:
         return "option3_2_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         slot_value = tracker.get_slot('newstock3')
         slot_value1 = tracker.get_slot('username')
         con = sqlite3.connect("../../Django/db.sqlite3")
         cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company_official='{}'".format(slot_value.upper()))
         row = cursor.fetchone()
         con.close()        

         if slot_value == "Invalid":
            return [SlotSet("newstock3", None)]
         else:
            x = requests.post("http://127.0.0.1:8000/option3_add/?stock={}&username={}&tick={}".format(slot_value,slot_value1,row[0]))
            buttons = [{"title": "Back to Menu", "payload": "/option3"}]
            button_type= "vertical"
            dispatcher.utter_message(text="{} is added to monitoring list.".format(slot_value),buttons=buttons,button_type=button_type)
            return [SlotSet("newstock3", None)]

class Option3_3(Action):
#
     def name(self) -> Text:
         return "option3_3_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         slot_value = tracker.get_slot('deletestock3')
         slot_value1 = tracker.get_slot('username')
         con = sqlite3.connect("../../Django/db.sqlite3")
         cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company_official='{}'".format(slot_value.upper()))
         row = cursor.fetchone()
         con.close()        

         if slot_value == "Invalid":
            return [SlotSet("deletestock3", None)]
         else:
            x = requests.post("http://127.0.0.1:8000/option3_delete/?stock={}&username={}&tick={}".format(slot_value,slot_value1,row[0]))
            buttons = [{"title": "Back to Menu", "payload": "/option3"}]
            button_type= "vertical"
            dispatcher.utter_message(text="{} is deleted from monitoring list.".format(slot_value),buttons=buttons,button_type=button_type)
            return [SlotSet("deletestock3", None)]

         return []

class Option4_1(Action):
#
     def name(self) -> Text:
         return "option4_1_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         slot_value = tracker.get_slot('firststock')
         stock1 = "{}.KL".format(slot_value)
         slot_value1 = tracker.get_slot('secondstock')
         stock2 = "{}.KL".format(slot_value1)
         month = tracker.get_slot('correlationmonth')
         #Get today date
         today = date.today()
         # YYYY-MM-DD
         d1 = today.strftime("%Y/%m/%d")
         startdate =  date.today() + relativedelta(months=-int(month))

         test = data.DataReader([stock1,stock2],'yahoo',start=startdate,end=d1)
         test = test['Adj Close']
         corr = (test[stock1].corr(test[stock2]))*100

         con = sqlite3.connect("../../Django/db.sqlite3")
         cursor = con.execute("SELECT company_official from rasa_chatbot_bursalist WHERE company_tickname='{}'".format(slot_value))
         row1 = cursor.fetchone()
         cursor = con.execute("SELECT company_official from rasa_chatbot_bursalist WHERE company_tickname='{}'".format(slot_value1))
         row2 = cursor.fetchone()
         con.close()  

         buttons = [{"title": "Back to Menu", "payload": "/option4"}]
         button_type= "vertical"
         dispatcher.utter_message(text="Correlation between {} and {} for last {} months is {:.0f}%.".format(row1[0],row2[0],month,corr),buttons=buttons,button_type=button_type)
         

         return [SlotSet("firststock", None),SlotSet("secondstock", None),SlotSet("correlationmonth", None)]

class Option4_2(Action):
#
     def name(self) -> Text:
         return "option4_2_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         slot_value = tracker.get_slot('vstock')
         stock1 = "{}.KL".format(slot_value)
         month = tracker.get_slot('vmonth')
         #Get today date
         today = date.today()
         # YYYY-MM-DD
         d1 = today.strftime("%Y/%m/%d")
         startdate =  date.today() + relativedelta(months=-int(month))

         test = data.DataReader(stock1,'yahoo',start=startdate,end=d1)
         test['Log return'] = np.log(test['Close']/test['Close'].shift())
         volatility = (test['Log return'].std()*252**.5)*100
         print(volatility)

         con = sqlite3.connect("../../Django/db.sqlite3")
         cursor = con.execute("SELECT company_official from rasa_chatbot_bursalist WHERE company_tickname='{}'".format(slot_value))
         row1 = cursor.fetchone()
         con.close()  

         buttons = [{"title": "Back to Menu", "payload": "/option4"}]
         button_type= "vertical"
         dispatcher.utter_message(text="Price Volatility of {} for last {} months is {:.0f}%.".format(row1[0],month,volatility),buttons=buttons,button_type=button_type)
         
         
         return [SlotSet("vstock", None),SlotSet("vmonth", None)]

class Option4_3(Action):
#
     def name(self) -> Text:
         return "option4_3_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         slot_value = tracker.get_slot('stocklist')
         slot_value = slot_value.split(',')
         con = sqlite3.connect("../../Django/db.sqlite3")
         ticklist=[]
         for stock in slot_value:
            cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company='{}'".format(stock.lower()))
            row = cursor.fetchone()
            ticklist.append(row[0]+".KL")
         #Get today date
         today = date.today()
         # YYYY-MM-DD
         d1 = today.strftime("%Y/%m/%d")
         startdate =  date.today() + relativedelta(months=-12)

         test = data.DataReader(ticklist,'yahoo',start=startdate,end=d1)
         test = test['Adj Close']
         p_ret = []
         p_vol = []
         p_weights = []
         num_assets = len(test.columns)
         num_portfolios = 10000
         cov_matrix = test.pct_change().apply(lambda x:np.log(1+x)).cov()
         ind_er = test.resample('Y').last().pct_change().mean()

         for portfolio in range(num_portfolios):
            weights = np.random.random(num_assets)
            weights = weights/np.sum(weights)
            p_weights.append(weights)
            returns = np.dot(weights,ind_er)

            p_ret.append(returns)
            var = cov_matrix.mul(weights,axis=0).mul(weights,axis=1).sum().sum()
            sd = np.sqrt(var)
            ann_sd = sd*np.sqrt(250)
            p_vol.append(ann_sd)
            data_1 = {'Returns':p_ret,'Volatility':p_vol}

         for counter, symbol in enumerate(test.columns.tolist()):
            cursor = con.execute("SELECT company_official from rasa_chatbot_bursalist WHERE company_tickname='{}'".format(symbol[:-3]))
            row = cursor.fetchone()
            data_1[row[0]] = [w[counter] for w in p_weights]
         
         portfolios = pd.DataFrame(data_1)
         #minimum volatility portfolio
         min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]
         msg = "Minimum Volatility Portfolio Allocation\n"
         for i,b in min_vol_port.items():
            msg = msg + "{} : {:.0f}%\n".format(i,b*100)

         msg = msg + "\nOptimal Risky Portfolio Allocation\n"
         #optimal risky portfolio
         rf = 0.01 #risk factor
         optimal_risky_port = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]
         for i,b in optimal_risky_port.items():
            msg = msg + "{} : {:.0f}%\n".format(i,b*100)
         buttons = [{"title": "Back to Menu", "payload": "/option4"}]
         button_type= "vertical"
         dispatcher.utter_message(text=msg,buttons=buttons,button_type=button_type)
         return [SlotSet("stocklist", None)]

class Option5_1(Action):
#
     def name(self) -> Text:
         return "option5_1_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         try:
            slot_value = tracker.get_slot('stockoption5')
            arima_p = tracker.get_slot('arima_parameters')
            #Get today date
            today = date.today()
            # YYYY-MM-DD
            d1 = today.strftime("%Y-%m-%d")
            startdate =  date.today() + relativedelta(months=-3)

            # Testing Accuracy
            df = yf.download("{}.KL".format(slot_value),start=startdate,end=d1)
            train_data, test_data = df[0:int(len(df)*0.7)], df[int(len(df)*0.7):]
            training_data = train_data['Close'].values
            test_data = test_data['Close'].values
            history = [x for x in training_data]
            model_predictions = []
            N_test_observations = len(test_data)
            for time_point in range(N_test_observations):
                model = ARIMA(history, order=(int(arima_p[0]),int(arima_p[1]),int(arima_p[2])))
                model_fit = model.fit(disp=0)
                output = model_fit.forecast()
                yhat = output[0]
                model_predictions.append(yhat)
                true_test_value = test_data[time_point]
                history.append(true_test_value)
            MSE_error = mean_squared_error(test_data, model_predictions)

            ### do it in future as it need database
            con = sqlite3.connect("../../Django/db.sqlite3")
            cursor = con.execute("SELECT company_official from rasa_chatbot_bursalist WHERE company_tickname='{}'".format(slot_value))
            row = cursor.fetchone()
            con.close()        

            msg = "Result of ARIMA({},{},{}) - {}\n".format(arima_p[0],arima_p[1],arima_p[2],row[0])
            msg = msg + 'Testing Mean Squared Error (Most recent 30% of data is testing dataset) : {:.3}\n\n'.format(MSE_error)

            #yahho finance - get current price
            string_check = "{}.KL".format(slot_value)
            yahoo_financials = YahooFinancials(string_check)
            current_price = yahoo_financials.get_current_price()
            msg = msg + "Current Price : {:.2f}\n\n".format(current_price)
            msg = msg + "Next 10 days prediction :\n"

            #Predict for next 10 days
            for time_point in range(10):
                model = ARIMA(history, order=(int(arima_p[0]),int(arima_p[1]),int(arima_p[2])))
                model_fit = model.fit(disp=0)
                output = model_fit.forecast()
                yhat = output[0]
                history.append(yhat)
                msg = msg + "Day {} : {:.2f}\n".format(time_point+1,yhat[0])
         
            buttons = [{"title": "Back to Menu", "payload": "/option5"}]
            button_type= "vertical"
            dispatcher.utter_message(text=msg,buttons=buttons,button_type=button_type)
            return [SlotSet("stockoption5", None),SlotSet("arima_parameters",None)]
         except:
            buttons = [{"title": "Back to Menu", "payload": "/option5"}]
            button_type= "vertical"
            dispatcher.utter_message(text="ARIMA is likelty unable to converge.Please re-try.",buttons=buttons,button_type=button_type)
            return [SlotSet("stockoption5", None),SlotSet("arima_parameters",None)]


class StockPickForm(FormValidationAction):

     def name(self) -> Text:
         return "validate_stockpick_form"

     def validate_stocktick(self, 
     	     slot_value: Any,
     	     dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         # check the stock name lookup
         ### do it in future as it need database
         authentication = tracker.get_slot('authentication')

         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return {"stocktick": None}
         else:
            con = sqlite3.connect("../../Django/db.sqlite3")
            cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company='{}'".format(slot_value.lower()))
            row = cursor.fetchone()
            con.close()        

            #if the name is not valid stock tick
            if  row==None:
                dispatcher.utter_message(text="Kindly only key in the tick name/Stock Name. \nEg. Seven Eleven/7-ELEVEN MALAYSIA HOLDINGS BERHAD")
                return {"stocktick": None}
            else:
                return {"stocktick": row[0]}

class AuthenticationForm(FormValidationAction):

     def name(self) -> Text:
         return "validate_authentication_form"

     def validate_username(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         #if the name is not valid stock tick
         con = sqlite3.connect("../../Django/db.sqlite3")
         cursor = con.execute("SELECT username from rasa_chatbot_userdatabase WHERE username='{}'".format(slot_value))
         row = cursor.fetchone()
         con.close()
         if row == None:
            dispatcher.utter_message(text="Username is not valid. Kindly contact admin")
            return {"username": None}
         else:
            dispatcher.utter_message(text="Hi, {}.".format(slot_value))
            return {"username": slot_value}

     def validate_password(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         #if the name is not valid stock tick
         con = sqlite3.connect("../../Django/db.sqlite3")
         cursor = con.execute("SELECT password from rasa_chatbot_userdatabase WHERE username='{}'".format(slot_value))
         row = cursor.fetchone()
         con.close()
         #if the name is not valid stock tick
         if row == None:
            dispatcher.utter_message(text="Password is not valid. Kindly contact admin")
            return {"password": None}
         else:
            #SlotSet("authentication", True)
            msg = "This is Stock Advisor Bot.\nPlease select one of the following options"
            buttons = [{"title": "1 Stock Information", "payload": "/option1"},
                       {"title": "2 Sentiment Analysis", "payload": "/option2"},
                       {"title": "3 Announcements", "payload": "/option3"},
                       {"title": "4 Portfolio Analysis", "payload": "/option4"},
                       {"title": "5 Stock Price Forecasting", "payload": "/option5"},
                       {"title": "6 Reinforcement Learning/Evolving Learning for Trading Strategies", "payload": "/option6"}]
            button_type= "vertical"
            dispatcher.utter_message(text=msg,buttons=buttons,button_type=button_type)
            return {"password": slot_value,"authentication": True}

class Option3_add(FormValidationAction):

     def name(self) -> Text:
         return "validate_option3_add_form"

     def validate_newstock3(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


         # check the stock name lookup
         ### do it in future as it need database
         authentication = tracker.get_slot('authentication')

         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return {"newstock3": None}
         else:
            # check the stock name lookup
            username = tracker.get_slot("username")
            ### do it in future as it need database
            con = sqlite3.connect("../../Django/db.sqlite3")
            cursor = con.execute("SELECT company_official from rasa_chatbot_bursalist WHERE company='{}'".format(slot_value.lower()))
            row = cursor.fetchone()
            if row==None:
                dispatcher.utter_message(text="Kindly only key in the tick name/Stock Name. \nEg. Seven Eleven/7-ELEVEN MALAYSIA HOLDINGS BERHAD")
                con.close()
                return {"newstock3": None}
            else:
                cursor = con.execute("SELECT company_official from rasa_chatbot_option3_stock_monitoring WHERE company_official='{}'".format(row[0]))
                check2 = cursor.fetchone()
                cursor = con.execute("SELECT company_official from rasa_chatbot_option3_stock_monitoring WHERE username='{}'".format(username))
                check3 = cursor.fetchall()
                con.close() 
                if len(check3)>10:
                    buttons = [{"title": "Back to Menu", "payload": "/option3"}]
                    button_type= "vertical"
                    dispatcher.utter_message(text="Maximum Stock for Monitoring is 10",buttons=buttons,button_type=button_type)
                    return {"newstock3": "Invalid"}
                elif check2:
                    buttons = [{"title": "Back to Menu", "payload": "/option3"}]
                    button_type= "vertical"
                    dispatcher.utter_message(text="Stock is existed in the Monitoring list",buttons=buttons,button_type=button_type)
                    return {"newstock3": "Invalid"}
                else:
                    return {"newstock3": row[0]}


class Option3_delete(FormValidationAction):

     def name(self) -> Text:
         return "validate_option3_delete_form"

     def validate_deletestock3(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         authentication = tracker.get_slot('authentication')

         # check the stock name lookup
         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return {"deletestock3": None}
         else:
            username = tracker.get_slot("username")
            ### do it in future as it need database
            con = sqlite3.connect("/../../Django/db.sqlite3")
            cursor = con.execute("SELECT company_official from rasa_chatbot_bursalist WHERE company='{}'".format(slot_value.lower()))
            row = cursor.fetchone()
            if row==None:
                dispatcher.utter_message(text="Kindly only key in the tick name/Stock Name. \nEg. Seven Eleven/7-ELEVEN MALAYSIA HOLDINGS BERHAD")
                con.close()
                return {"deletestock3": None}
            else:
                cursor = con.execute("SELECT company_official from rasa_chatbot_option3_stock_monitoring WHERE company_official='{}' AND username='{}'".format(row[0],username))
                check2 = cursor.fetchone()
                con.close() 
                if check2==None:
                    buttons = [{"title": "Back to Menu", "payload": "/option3"}]
                    button_type= "vertical"
                    dispatcher.utter_message(text="Stock is not existed in the Monitoring list",buttons=buttons,button_type=button_type)
                    return {"deletestock3": "Invalid"}
                else:
                    return {"deletestock3": row[0]}

class Option4_correlation(FormValidationAction):

     def name(self) -> Text:
         return "validate_option4_correlation_form"

     def validate_firststock(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         authentication = tracker.get_slot('authentication')

         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return {"firststock": None}
         else:
            # check the stock name lookup
            ### do it in future as it need database
            con = sqlite3.connect("../../Django/db.sqlite3")
            cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company='{}'".format(slot_value.lower()))
            row = cursor.fetchone()
            con.close()        
            #if the name is not valid stock tick
            if  row==None:
                dispatcher.utter_message(text="Kindly only key in the tick name/Stock Name. \nEg. Seven Eleven/7-ELEVEN MALAYSIA HOLDINGS BERHAD")
                return {"firststock": None}
            else:
                return {"firststock": row[0]}

     def validate_secondstock(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         
         # check the stock name lookup
         ### do it in future as it need database
         con = sqlite3.connect("../../Django/db.sqlite3")
         cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company='{}'".format(slot_value.lower()))
         row = cursor.fetchone()
         con.close()        

         #if the name is not valid stock tick
         if  row==None:
            dispatcher.utter_message(text="Kindly only key in the tick name/Stock Name. \nEg. Seven Eleven/7-ELEVEN MALAYSIA HOLDINGS BERHAD")
            return {"secondstock": None}
         else:
            return {"secondstock": row[0]}

     def validate_correlationmonth(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         
         # check the stock name lookup
         ### do it in future as it need database
         if not slot_value.isnumeric():
            dispatcher.utter_message(text="Only Numeric Number is allowed")     
            return {"correlationmonth": None}
         elif  int(slot_value)>12:
            dispatcher.utter_message(text="Maximum month for correlation analysis is 12")
            return {"correlationmonth": None}
         elif int(slot_value)<1:
            dispatcher.utter_message(text="minimum month for correlation analysis is 1")
            return {"correlationmonth": None}
         else:
            return {"correlationmonth": slot_value}

class Option4_price_volatility(FormValidationAction):

     def name(self) -> Text:
         return "validate_option4_price_volatility_form"

     def validate_vstock(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         authentication = tracker.get_slot('authentication')

         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return {"vstock": None}
         else:
            # check the stock name lookup
            ### do it in future as it need database
            con = sqlite3.connect("../../Django/db.sqlite3")
            cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company='{}'".format(slot_value.lower()))
            row = cursor.fetchone()
            con.close()        

            #if the name is not valid stock tick
            if  row==None:
                dispatcher.utter_message(text="Kindly only key in the tick name/Stock Name. \nEg. Seven Eleven/7-ELEVEN MALAYSIA HOLDINGS BERHAD")
                return {"vstock": None}
            else:
                return {"vstock": row[0]}

     def validate_vmonth(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         
         # check the stock name lookup
         ### do it in future as it need database
         if not slot_value.isnumeric():
            dispatcher.utter_message(text="Only Numeric Number is allowed")     
            return {"vmonth": None}
         elif  int(slot_value)>12:
            dispatcher.utter_message(text="Maximum month for correlation analysis is 12")
            return {"vmonth": None}
         elif int(slot_value)<1:
            dispatcher.utter_message(text="minimum month for correlation analysis is 1")
            return {"vmonth": None}
         else:
            return {"vmonth": slot_value}

class Option4_portfolio(FormValidationAction):

     def name(self) -> Text:
         return "validate_option4_portfolio_form"

     def validate_stocklist(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         authentication = tracker.get_slot('authentication')
   
         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return {"stocklist": None}
         else:
            # check the stock name lookup
            slot_value = slot_value.lower()
            stocklist=slot_value.split(',')

            # connect to datbase
            con = sqlite3.connect("../../Django/db.sqlite3")

            if len(stocklist)<10: 
                for stock in stocklist:
                    cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company='{}'".format(stock.lower()))
                    row = cursor.fetchone()
                    if row == None:
                        dispatcher.utter_message(text="{} is invalid stockname/tick.".format(stock))
                        con.close()
                        return {"stocklist": None}
            else:
                dispatcher.utter_message(text="Currently, it only support maximum 10 stocks to compute optimal portforlio optimization".format(stock))
                con.close()
                return {"stocklist": None}
            con.close()
            dispatcher.utter_message(text="Please be patient. Computing Minimum Volatility Portfolio and Optimal Risky Portfolio!".format(stock))
            return {"stocklist":slot_value}

class Option5_stock(FormValidationAction):

     def name(self) -> Text:
         return "validate_option5_stock_form"

     def validate_stockoption5(self, 
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         authentication = tracker.get_slot('authentication')

         if authentication == False:
            buttons = [{"title": "Authentication", "payload": "/start"}]
            button_type= "vertical"
            dispatcher.utter_message(text="Hi, your session might be expired. Kindly key in your username and password again.",buttons=buttons,button_type=button_type)
            return {"stockoption5": None}
         else:
            # check the stock name lookup
            ### do it in future as it need database
            con = sqlite3.connect("../../Django/db.sqlite3")
            cursor = con.execute("SELECT company_tickname from rasa_chatbot_bursalist WHERE company='{}'".format(slot_value.lower()))
            row = cursor.fetchone()
            con.close()        

            #if the name is not valid stock tick
            if  row==None:
                dispatcher.utter_message(text="Kindly only key in the tick name/Stock Name. \nEg. Seven Eleven/7-ELEVEN MALAYSIA HOLDINGS BERHAD")
                return {"stockoption5": None}
            else:
                return {"stockoption5": row[0]}

     def validate_arima_parameters(self,
             slot_value: Any,
             dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         slot_value=slot_value[6:-1].split(",")

         # check the format
         for value in slot_value:
            print(value)
            if not value.isnumeric():
                dispatcher.utter_message(text="Format is invalid.Kindly follow the following format : eg ARIMA(1,1,0)")
                return {"arima_parameters": None}
          
         dispatcher.utter_message(text="Please be patient. Bot is computing ARIMA forecasting!")
         return {"arima_parameters": slot_value}


        









            
            




