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
#
#
class Option11_Price(Action):
#
     def name(self) -> Text:
         return "option1_response"
#
     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         #check stock tick name lookup - pandas

         #yahho finance
         slot_value = tracker.get_slot('stocktick')
         yahoo_financials = YahooFinancials(slot_value)
         current_price=yahoo_financials.get_current_price()
         current_change = round(yahoo_financials.get_current_change(),2)
         current_change_percent = yahoo_financials.get_current_percent_change()*100

         #trading_view_link
         tradingviewlink ="https://www.tradingview.com/chart/?symbol={}".format(slot_value)

         msg = "**{}** :\n\n**Price**\nCurrent Price: {}\nChanges: {:.2f}({:.2f}%)\nPrevious Close Price:\nOpen Price:\n\n**Volume**\n\n**Trading Views** :\n{}".format(slot_value,current_price,current_change,current_change_percent,tradingviewlink)

         buttons = [{"title": "Back to Menu", "payload": "/start"}]
         dispatcher.utter_message(text=msg,buttons=buttons)
         
         #dispatcher.utter_button_template(buttons)

         return [SlotSet("stocktick", None)]

#class Option1_backMenu(Action):
#
#     def name(self) -> Text:
#         return "option1_backMenu"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         #check stock tick name lookup - sqlite(Django)
         

         #trading view link
 #        dispatcher.utter_message(text="Please say ""Hi"" again to start new session")
         #dispatcher.utter_message(text=msg)

 #        return [SlotSet("stocktick", None)]

#class Option11_tradingview(Action):
#
#     def name(self) -> Text:
#         return "option1_tradingview"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         slot_value = tracker.get_slot('stocktick')
#         tradingviewlink ="https://www.tradingview.com/chart/?symbol={}".format(slot_value)
#         #trading view link
#         dispatcher.utter_custom_json('link: [tradingview](tradingviewlin)', parse_mode='markdown')
         #dispatcher.utter_message(text=msg)

#         return [SlotSet("stocktick", None)]

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

         #if the name is not valid stock tick
         if  len(slot_value)>10:
         	dispatcher.utter_message(text="Kindly only key in the tick name. Eg. APPL")
         	return {"stocktick": None}
         else:
         	return {"stocktick": slot_value}




