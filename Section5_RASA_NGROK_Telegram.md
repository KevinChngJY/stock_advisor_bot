# Milestone 1.2 RASA + Ngrok + Telegram

Objective : Set up Server in the host machine and connect to Telegram Chatbot.<br>
In this milestone, we are looking to set up telegram chatbot using BotFather, you may refer to the following link (https://telegram.org/blog/bot-revolution) to understand the chatbot in Telegram. As Rasa OpenSource Server and Action Server are running locally, therefore it requires ngrok to portfoward the traffic (secured) connect to Telegram.

---

## SECTION 1 : Architecture 

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/Screenshot%202021-08-29%20at%204.32.06%20PM.png" width="855" height="210"
     style="float: left; margin-right: 0px;" />

---

## SECTION 2 : Pre-requisite (Install Ngrok)

### What is ngrok?
Ngrok exposes local servers behind NATs and firewalls to the public internet over secure tunnels.

Website for ngrok : https://ngrok.com/

Install ngrok from : https://ngrok.com/download

---

## SECTION 3 : Set up Telegram Bot (Bot Father)

Article from Sendpulse illustrate very good flow to set up telegram chatbot using Bot Father (Do not need connect to Sendpulse)
The article will lead you to get the token for your telegram chatbot, then we will use this token for webhook in RASA.

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/scr8-min.png" width="555" height="410"
     style="float: left; margin-right: 0px;" />



