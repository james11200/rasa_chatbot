from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import time
import json


class AskWhichBranchAction(Action):
    def name(self) -> Text:
        return "action_ask_which_branch"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"title": "Xindian", "payload": "/Xindian"},
            {"title": "Zhonghe", "payload": "/Zhonghe"}
        ]
        dispatcher.utter_message(text=f"Here are some options: ", buttons=buttons)

        return []
# from actions import increment_dayoff_count

def increment_dayoff_count(json_file, user_id, increment_by):
    increment_by = int(increment_by)
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        users = data.get('users', [])
        user_found = False
        updated_day_off_count = None
        
        for user in users:
            if user.get('id') == user_id:
                # user['day_off_count'] = user.get('day_off_count', 0) + increment_by
                # user_found = True
                current_day_off_count = user.get('day_off_count', 0)
                user['day_off_count'] = int(current_day_off_count) + increment_by
                updated_day_off_count = user['day_off_count']
                
                user_found = True                
                break
        
        if not user_found:
            new_user = {"id": user_id, "day_off_count": increment_by}
            users.append(new_user)
            updated_day_off_count = user['day_off_count']
        
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=2)
        
        if user_found:
            print(f"{user_id} incremented by {increment_by}")
            # return f"Day off count for user {user_id} incremented by {increment_by} successfully."
            return updated_day_off_count
        else:
            print(f"{user_id} not found, added {user_id} with {increment_by}")
            # return f"User {user_id} not found. Added as a new user with {increment_by} day-offs."
            return updated_day_off_count
        
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Invalid JSON format."
    except Exception as e:
        return f"An error occurred while running increment_dayoff_count.py: {e}"





class IncrementDayoffCountAction(Action):
    def name(self) -> Text:
        return "action_increment_dayoff_count"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text=f"Hi {user_id}")
        
        try:            
            user_id = tracker.get_slot("user_id")  # specifically fetches the value of the slot 'user_id' set in the conversation context.
            # user_id = next(tracker.get_latest_entity_values('user_id'),None) #fetches the most recent 'user_id' entity value detected, which might not necessarily be stored in a slot.
            
            # if user_id:
            #     pass
            #     dispatcher.utter_message(text=f"Hi user {user_id}")
            # else:
            #     dispatcher.utter_message(text='no user_id')
            
            # increment_value = tracker.get_slot("increment_value")  
            increment_value = next(tracker.get_latest_entity_values('increment_value'),None) 
            
            # if increment_value:
            #     dispatcher.utter_message(text=f"working on request value: {increment_value}")
            # else:
            #     dispatcher.utter_message(text='no increment_value')            
            # dispatcher.utter_message(text=f"id: {user_id}, value: {increment_value}")
            
            # Path to your JSON file containing user data
            json_file_path = 'user_data.json'

            # Perform the incrementation using the function
            
            updated_day_off_count = increment_dayoff_count(json_file_path, user_id, increment_value)

            # dispatcher.utter_message(f"Day-off count {increment_value} updated successfully.")

            if updated_day_off_count is not None:
                dispatcher.utter_message(f"{increment_value} days Day-off count updated successfully. New count: {updated_day_off_count}")
            else:
                dispatcher.utter_message("Failed to update the day-off count.")

        except Exception as e:
            dispatcher.utter_message(f"An error occurred while running actions.py: {e}")

        return [SlotSet("updated_day_off_count", updated_day_off_count)]
