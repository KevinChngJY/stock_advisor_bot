from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.response import Response
from django.template import loader
from rest_framework import status
import requests
from django.views.decorators.csrf import csrf_exempt
from .models import option3_stock_monitoring,sentimentanalysistop10,userdatabase,bursalist

#Import for RL
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

# Create your views here.
@csrf_exempt
def option3_add(request):
	stock = request.GET['stock']
	username = request.GET['username']
	tick = request.GET['tick']
	q = option3_stock_monitoring(username=username,company_official=stock,company_tickname=tick,exchange="bursa")
	q.save()
	return Response({"UPDATE":"SUCCESS"}, status=status.HTTP_200_OK)


@csrf_exempt
def option3_delete(request):
	stock = request.GET['stock']
	username = request.GET['username']
	tick = request.GET['tick']
	print(username)
	print(stock)
	option3_stock_monitoring.objects.get(username=username,company_official=stock).delete()
	return Response({"UPDATE":"SUCCESS"}, status=status.HTTP_200_OK)

def option6_login(request):
	if request.method == 'POST' and "Login" in request.POST:
		username = request.POST.get('u')
		password = request.POST.get('p')
		userdatabase.objects.get(username=str(username))
		userdatabase.objects.get(password=str(password))
		try:
			username = request.POST.get('u')
			password = request.POST.get('p')
			userdatabase.objects.get(username=str(username))
			userdatabase.objects.get(password=str(password))
			return HttpResponse(render(request,"option6.html"))
		except:
			template = loader.get_template('index.html')
			explain = "Invalid Username/Password"
			context = {'explain':explain}
			return HttpResponse(template.render(context,request))
	if request.method == 'POST' and "Compute" in request.POST:
		try:
			stock_tick_name = request.POST.get('s')
			stock=bursalist.objects.get(company=str(stock_tick_name))
		except:
			template = loader.get_template('option6.html')
			explain = "Invalid Stock Tick Name"
			context = {'explain':explain}
			return HttpResponse(template.render(context,request))
		
		window_size = request.POST.get('w')
		episode_count = request.POST.get('e')
		if window_size.isdigit()==False or episode_count.isdigit()==False:
			template = loader.get_template('option6.html')
			explain = "Window Size & Episode must be digit!"
			context = {'explain':explain}
			return HttpResponse(template.render(context,request))

		# Train Agent for RL
		stock_tick = stock.company_tickname
		data_stock = getStockDataVec(stock_tick)
		window_size = int(window_size)
		episode_count = int(episode_count)
		agent = Agent(window_size)
		l = len(data_stock)-1
		print(l)
		batch_size = 32
		for e in range(episode_count + 1):
			print("Episode" + str(e) + "/" + str(episode_count))
			state = getState(data_stock,0,window_size+1)
			total_profit = 0
			agent.inventory = []
			for t in range(l):
				action = agent.act(state)
				next_state = getState(data_stock,t+1,window_size+1)
				reward = 0
				if action == 1:
					agent.inventory.append(data_stock[t])
					print("Buy: " + formatPrice(data_stock[t]))
				elif action ==2 and len(agent.inventory)>0:
					bought_price = agent.inventory.pop(0)
					reward = max(data_stock[t] - bought_price, 0)
					total_profit += data_stock[t] - bought_price
					print("Sell: " + formatPrice(data_stock[t]) + " | Profit: " + formatPrice(data_stock[t] - bought_price))
				done = True if t==1 else False
				agent.memory.append((state, action, reward, next_state, done))
				state = next_state
				if done:
					print("--------------------------------")
					print("Total Profit: " + formatPrice(total_profit))
					print("--------------------------------")
				if len(agent.memory) > batch_size:
					agent.expReplay(batch_size)

		# RL Evaluation
		state = getState(data_stock,0,window_size+1)
		total_profit = 0
		agent.inventory = []
		for t in range(l):
			action = agent.act(state)
			print(action)
			# sit
			next_state = getState(data, t + 1, window_size + 1)
			reward = 0
			if action == 1: # buy
				agent.inventory.append(data[t])
				print("Buy: " + formatPrice(data[t]))
			elif action == 2 and len(agent.inventory) > 0: # sell
				bought_price = agent.inventory.pop(0)
				reward = max(data[t] - bought_price, 0)
				total_profit += data[t] - bought_price
				print("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
			done = True if t == l - 1 else False
			agent.memory.append((state, action, reward, next_state, done))
			state = next_state

		# GA Optimization
	return HttpResponse(render(request,"index.html"))

# Agent
class Agent:
    def __init__(self,state_size,is_eval=False,model_name=""):
        self.state_size = state_size # normalized previous day
        self.action_size = 3 # sit,buy, sell
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
        if not self.is_eval and random.random()<= self.epsilon:
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
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Basic Function
def formatPrice(n):
    return("-Rs." if n<0 else "Rs.")+"{0:.2f}".format(abs(n))
def getStockDataVec(key):
	stock1 = "{}.KL".format(key)
	#Get today date
	today = date.today()
	# YYYY-MM-DD
	d1 = today.strftime("%Y/%m/%d")
	startdate =  date.today() + relativedelta(months=-int(12))
	test = data.DataReader(stock1,'yahoo',start=startdate,end=d1)
	vec = list(test['Close'])
	return vec 
def sigmoid(x):
    return 1/(1+math.exp(-x))
def getState(data, t, n):
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1] # pad with t0
    res = []
    for i in range(n - 1):
        res.append(sigmoid(block[i + 1] - block[i]))
    return np.array([res])


#Train RL
#def run_rl(tick_name):

