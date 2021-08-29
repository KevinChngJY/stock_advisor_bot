# Milestone 1.1 RASA

---

## SECTION 1 : Pre-requisites

1) Kindly install anaconda in your computer:
https://docs.anaconda.com/anaconda/install/index.html

2) Instal the following packages in your conda environment:
```
pip install rasa[full]
pip install yahoofinancials
```

Documentation for RASA : https://rasa.com/ <br>
Documentatoion for yahoofinancials : https://pypi.org/project/yahoofinancials/ <br>

---

## Section 2 : Guide to familiar RASA
[You may skip this part if it is irrelevant to you]

Medium : https://medium.com/analytics-vidhya/build-a-chatbot-using-rasa-78406306aa0c <br>
RASA playground : https://rasa.com/docs/rasa/playground/

---

## Section 3 : Download the milestone 1 project - material

Download the entire project from https://github.com/KevinChngJY/stock_advisor_bot <br>
Open command prompt and navigate to Milestone1 (folder inside the downloaded files). <br>

---

## Section 4 : Run the RASA + RASA Action Server

Run Rasa Action Server
```
rasa run actions
```

Run Rasa Shell
```
rasa shell -v
```

Now you can type the following conversation in the rasa shell to test it out:

<img src="https://github.com/KevinChngJY/stock_advisor_bot/blob/main/Image/Chat1.png" width="500" height="400"
     style="float: left; margin-right: 0px;" />
