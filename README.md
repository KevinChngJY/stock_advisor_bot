
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
| 3.1 Authentication Login In | | |
| 3.2 Database (Django) |  |  |
| 3.3 RASA + Django + Celery + Database | | |
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

Functional Architecture:
