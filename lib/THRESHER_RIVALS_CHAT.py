import pyautogui
import keyboard
import time
import re
import random


## marvel_rivals_commands = ("type in chat", "type in rivals", "type in team", "type in faction", "type in match")
censored_swears = ("fuck", "shit", "bullshit", "motherfucker", "fucker", "bitch", "cunt", "ass", "bastard")
censor_symbols = ("!", "@", "#", "$", "%", "^", "&", "*")
chat_type = ""


def chat(message_type, passed_command):
    try:
        match = re.search(r"(type (?:and|in) (?:rivals|team|faction|match) chat)|(type in (?:rivals|team|faction|match))|(match chat)|(type in chat)|(type(?: and chat)?)|(chat)", passed_command)
        if match:
            if match.group(1):  # Handles "type (and|in) X chat"
                target = match.group(2) + " chat"
                message = passed_command.replace(match.group(1), "").strip()
            elif match.group(2):  # Handles "type in X"
                target = match.group(2)
                message = passed_command.replace(match.group(2), "").strip()
            elif match.group(3):  # Handles "match chat"
                target = "match chat"
                message = passed_command.replace("match chat", "").strip()
            elif match.group(4):  # Handles "type in chat"
                target = "chat"
                message = passed_command.replace("type in chat", "").strip()
            elif match.group(5):  # Handles "type (and chat)"
                target = "generic" # Or a more appropriate type
                message = passed_command.replace(match.group(5), "").strip()
            elif match.group(6): # Handles "chat" on its own
                target = "generic"
                message = passed_command.replace("chat", "").strip()
            send_chat_message(message_type, message)  # Or message_type if it's relevant
        else:
            message = passed_command
            send_chat_message("generic", message)
    except Exception as e:
        print(f"Error processing chat command: {e}")



def send_chat_message(message_type, message):
    try:
        message = censor_swear(message)

        pyautogui.press('enter')
        time.sleep(0.2)

        keyboard.write(message)  # Use keyboard.write()
        time.sleep(0.5)

        pyautogui.press('enter')
        time.sleep(0.2)

        pyautogui.press('enter')
        time.sleep(0.2)

        print("Message sent successfully.")

    except Exception as e:
        print(f"Error sending message: {e}")



def censor_swear(message):
    words = message.split()
    censored_words = []
    for word in words:
        for swear in censored_swears:
            if swear in word.lower():  # Case-insensitive check
                censored_word = ""
                for char in word:
                    if char.lower() in swear: #Censors only the swear part of the word
                        censored_word += random.choice(censor_symbols)
                    else:
                        censored_word += char
                censored_words.append(censored_word)
                break  # Stop checking other swears if one is found
        else:  # No swear word found
            censored_words.append(word)

    return " ".join(censored_words)