from django.shortcuts import render, redirect
from django.http import HttpResponse
from keras.backend import prod
from rest_framework.response import Response
from django.template import loader
from rest_framework import status
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import option3_stock_monitoring, sentimentanalysistop10, userdatabase, bursalist

# Import for RL
import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import math
import numpy as np
import random
from collections import deque
import sys
from datetime import date
from dateutil.relativedelta import relativedelta
from pandas_datareader import data

# Import for GA
import tagenalgo as tg
from tagenalgo import TAGenAlgo
from sklearn.model_selection import train_test_split
from ta.momentum import RSIIndicator


# Create your views here.


@csrf_exempt
def option3_add(request):
    stock = request.GET['stock']
    username = request.GET['username']
    tick = request.GET['tick']
    q = option3_stock_monitoring(
        username=username, company_official=stock, company_tickname=tick, exchange="bursa")
    q.save()
    return Response({"UPDATE": "SUCCESS"}, status=status.HTTP_200_OK)


@csrf_exempt
def option3_delete(request):
    stock = request.GET['stock']
    username = request.GET['username']
    tick = request.GET['tick']
    print(username)
    print(stock)
    option3_stock_monitoring.objects.get(
        username=username, company_official=stock).delete()
    return Response({"UPDATE": "SUCCESS"}, status=status.HTTP_200_OK)


def option6_login(request):
    # Check for Username and Password
    if request.method == 'POST' and "Login" in request.POST:
        username = request.POST.get('u')
        password = request.POST.get('p')
        try:
            username = request.POST.get('u')
            password = request.POST.get('p')
            userdatabase.objects.get(username=str(username))
            userdatabase.objects.get(password=str(password))
            return HttpResponse(render(request, "option6.html"))
        except:
            template = loader.get_template('index.html')
            explain = "Invalid Username/Password"
            context = {'explain': explain}
            return HttpResponse(template.render(context, request))
    if request.method == 'POST' and "Compute" in request.POST:

        # Check for stock tick name
        try:
            stock_tick_name = request.POST.get('s')
            stock = bursalist.objects.get(company=str(stock_tick_name))
        except:
            template = loader.get_template('option6.html')
            explain = "Invalid Stock Tick Name"
            context = {'explain': explain}
            return HttpResponse(template.render(context, request))

        # Check for key_in for window size and episode count (Must be digit)
        window_size = request.POST.get('w')
        episode_count = request.POST.get('e')
        number_generation = request.POST.get('ga')
        if window_size.isdigit() == False or episode_count.isdigit() == False:
            template = loader.get_template('option6.html')
            explain = "Window Size & Episode must be digit!"
            context = {'explain': explain}
            return HttpResponse(template.render(context, request))

        # Check for window_size
        if int(window_size) < 5 or int(window_size) > 20:
            template = loader.get_template('option6.html')
            explain = "Window Size must be between 5 and 20"
            context = {'explain': explain}
            return HttpResponse(template.render(context, request))

        # Check for episode count
        if int(episode_count) < 1 or int(episode_count) > 5:
            template = loader.get_template('option6.html')
            explain = "System is running in personal home laptop, so maximum epsiode is 5"
            context = {'explain': explain}
            return HttpResponse(template.render(context, request))

        # Check for number GA
        if int(number_generation) < 1 or int(number_generation) > 5:
            template = loader.get_template('option6.html')
            explain = "System is running in personal home laptop, so maximum generation is 5"
            context = {'explain': explain}
            return HttpResponse(template.render(context, request))

        # Train Agent for RL
        print("Start RL Training")

        stock_tick = stock.company_tickname
        data_stock, date_data = getStockDataVec(stock_tick)
        window_size = int(window_size)
        episode_count = int(episode_count)
        agent = Agent(window_size)
        l = len(data_stock)-1
        # # print(l)
        batch_size = 32
        for e in range(episode_count + 1):
            print("Episode" + str(e) + "/" + str(episode_count))
            state = getState(data_stock, 0, window_size+1)
            total_profit = 0
            agent.inventory = []
            for t in range(l):
                print(date_data[t])
                action = agent.act(state)
                next_state = getState(data_stock, t+1, window_size+1)
                reward = 0
                if action == 1:
                    agent.inventory.append(data_stock[t])
                    print("Buy: " + formatPrice(data_stock[t]))
                elif action == 2 and len(agent.inventory) > 0:
                    bought_price = agent.inventory.pop(0)
                    reward = max(data_stock[t] - bought_price, 0)
                    total_profit += data_stock[t] - bought_price
                    print("Sell: " + formatPrice(data_stock[t]) + " | Profit: " + formatPrice(
                        data_stock[t] - bought_price))
                done = True if t == l-1 else False
                agent.memory.append((state, action, reward, next_state, done))
                state = next_state
                if done:
                    print("--------------------------------")
                    print("Total Profit: " + formatPrice(total_profit))
                    print("--------------------------------")
                if len(agent.memory) > batch_size:
                    agent.expReplay(batch_size)

        # # RL Evaluation
        print("Start RL Evaluation")

        state = getState(data_stock, 0, window_size+1)
        total_profit = 0
        agent.inventory = []
        action_show_RL = []
        cummulated_show_profit = []
        for t in range(l):
            print(date_data[t])
            action = agent.act(state)
            # sit
            next_state = getState(data_stock, t + 1, window_size + 1)
            reward = 0
            if action == 1:  # buy
                agent.inventory.append(data_stock[t])
                print("Buy: " + formatPrice(data_stock[t]))
                action_show_RL.append("Buy")
            elif action == 2 and len(agent.inventory) > 0:  # sell
                bought_price = agent.inventory.pop(0)
                reward = max(data_stock[t] - bought_price, 0)
                total_profit += data_stock[t] - bought_price
                action_show_RL.append("Sell")
                print(
                    "Sell: " + formatPrice(data_stock[t]) + " | Profit: " + formatPrice(data_stock[t] - bought_price))
            else:
                action_show_RL.append("No Action")
            done = True if t == l - 1 else False
            if done:
                print("--------------------------------")
                print("Total Profit: " + formatPrice(total_profit))
                print("--------------------------------")
            agent.memory.append((state, action, reward, next_state, done))
            state = next_state
            cummulated_show_profit.append(total_profit)

        # GA Optimization
        # GA Training
        print("Start GA Trainng")

        data_stock1 = np.array(data_stock)
        model = TAGenAlgo(price=data_stock1, generations=int(number_generation), population_size=100,
                          crossover_prob=0.9, mutation_prob=0, method='single', strategy='rsi')
        _, init_pop = model.ta_initialize(indicator_set={
                                          'rsi': {'window': [5, 180], 'down_thres': [5, 50], 'up_thres': [51, 90]}})
        model.fit(init_pop)
        best_window, best_lower_rsi, best_upper_rsi = model.best_params

        # Evaluate GA
        print("Start GA Evaluation")
        df = getStockDataVec_GA(stock_tick)
        indicator_rsi = RSIIndicator(
            close=df,  window=best_window, fillna=True)
        df['rsi'] = indicator_rsi.rsi()
        slicing_len = len(data_stock)
        df = df[-slicing_len:]
        action_show_GA = []
        cummulated_show_ga_profit = []
        total_profit_GA = 0
        inventory = []
        for count, t in enumerate(range(l)):
            print(date_data[t])
            inventory = []
            if df['rsi'][count] < best_lower_rsi:  # buy
                inventory.append(data_stock[t])
                print("Buy: " + formatPrice(data_stock[t]))
                action_show_GA.append("Buy")
            # sell
            elif df['rsi'][count] > best_upper_rsi and len(inventory) > 0:
                bought_price = inventory.pop(0)
                reward = max(data_stock[t] - bought_price, 0)
                total_profit_GA += data_stock[t] - bought_price
                action_show_RL.append("Sell")
                print(
                    "Sell: " + formatPrice(data_stock[t]) + " | Profit: " + formatPrice(data_stock[t] - bought_price))
            else:
                action_show_GA.append("No Action")
            cummulated_show_ga_profit.append(total_profit_GA)

        # Buy or Sell - Advise
        rl_advise = action_show_GA[-1]
        ga_advise = action_show_RL[-1]

        # tidy variables (Sent to frontend)
        data_stock = ["{0:.3f}".format(x)for x in data_stock]
        cummulated_show_profit = ["{0:.3f}".format(
            x)for x in cummulated_show_profit]
        cummulated_show_ga_profit = ["{0:.3f}".format(
            x)for x in cummulated_show_ga_profit]
        table_value = zip(date_data, data_stock,
                          action_show_RL, cummulated_show_profit,
                          action_show_GA, cummulated_show_ga_profit)
        official_name = stock.company_official
        context = {'table_value': table_value, 'official_name': official_name, 'episode_count': episode_count, 'total_profit': "{0:.3f}".format(total_profit),
                   'number_generation': number_generation, 'best_window': best_window, 'best_lower_rsi': best_lower_rsi, 'best_upper_rsi': best_upper_rsi,
                   'total_profit_GA': "{0:.3f}".format(total_profit_GA), 'rl_advise': rl_advise, 'ga_advise': ga_advise}
        template = loader.get_template('option6_compute.html')
        return HttpResponse(template.render(context, request))

    return HttpResponse(render(request, "index.html"))

# Agent-RL


class Agent:
    def __init__(self, state_size, is_eval=False, model_name=""):
        self.state_size = state_size  # normalized previous day
        self.action_size = 3  # sit,buy, sell
        self.memory = deque(maxlen=1000)
        self.inventory = []
        self.model_name = model_name
        self.is_eval = is_eval
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.model = load_model(model_name) if is_eval else self._model()

    def _model(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.state_size, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        return model

    def act(self, state):
        if not self.is_eval and random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        options = self.model.predict(state)
        return np.argmax(options[0])

    def expReplay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        for i in range(l - batch_size + 1, l):
            mini_batch.append(self.memory[i])
        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                    np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Basic Function for RL


def formatPrice(n):
    return("-Rs." if n < 0 else "Rs.")+"{0:.2f}".format(abs(n))


def getStockDataVec(key):
    stock1 = "{}.KL".format(key)
    # Get today date
    today = date.today()
    # YYYY-MM-DD
    d1 = today.strftime("%Y/%m/%d")
    startdate = date.today() + relativedelta(months=-int(3))
    test = data.DataReader(stock1, 'yahoo', start=startdate, end=d1)
    vec = list(test['Close'])
    vec = [float("{0:.3f}".format(x)) for x in vec]
    date_data = list(test.index)
    date_data = [d.strftime('%y-%m-%d') for d in date_data]
    return vec, date_data


def sigmoid(x):
    return 1/(1+math.exp(-x))


def getState(data, t, n):
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * \
        [data[0]] + data[0:t + 1]  # pad with t0
    res = []
    for i in range(n - 1):
        res.append(sigmoid(block[i + 1] - block[i]))
    return np.array([res])

# Basic Function for GA


def getStockDataVec_GA(key):
    stock1 = "{}.KL".format(key)
    # Get today date
    today = date.today()
    # YYYY-MM-DD
    d1 = today.strftime("%Y/%m/%d")
    startdate = date.today() + relativedelta(months=-int(4))
    test = data.DataReader(stock1, 'yahoo', start=startdate, end=d1)
    vec = test['Close']
    return vec
