import json

def increment_dayoff_count(json_file, user_id, increment_by):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        users = data.get('users', [])
        user_found = False
        
        for user in users:
            if user.get('id') == user_id:
                user['day_off_count'] = user.get('day_off_count', 0) + increment_by
                user_found = True
                break
        
        if not user_found:
            new_user = {"id": user_id, "day_off_count": increment_by}
            users.append(new_user)
        
        with open(json_file, 'w') as file:
            json.dump(data, file, indent=2)
        
        if user_found:
            return f"Day off count for user {user_id} incremented by {increment_by} successfully."
        else:
            return f"User {user_id} not found. Added as a new user with {increment_by} day-offs."
        
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Invalid JSON format."
    except Exception as e:
        return f"An error occurred while running increment_dayoff_count.py: {e}"
