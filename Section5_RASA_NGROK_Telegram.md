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

Link: <br>
https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/scr8-min.png" width="555" height="610"
     style="float: left; margin-right: 0px;" />

---

## SECTION 4 : Configure Rasa Credential File

In the root folder of RASA, open credentials.yml. <br>
Add the following telegram line : <br>

At this moment, we don't have the ngrok link as we have not yet run ngrok. 

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/credentiasyml.png" width="635" height="410"
     style="float: left; margin-right: 0px;" />

(Put your own token to the link in the above diagram)

Besides, you have to change the chatbot name for the verify in the above diagram.

---

## SECTION 5 : Run ngrok and configure RASA Credential File

Open terminal, run
```
ngrok http 5005
```

Then you would see the outcome as follows:

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/runngrok.png" width="635" height="210"
     style="float: left; margin-right: 0px;" />

Copy the https ngrok link in the diagram above and paste into the credential file:

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/credential2.png" width="635" height="510"
     style="float: left; margin-right: 0px;" />

Take note that you have to put /webhooks/telegram/webhook behind the ngrok link. 



