## Project THRESHER - THINKING HIGH-SPEED RESPONSIVE EXECUTIVE SYSTEM for HUMAN EFFICENCY and RESPONSE
## Inspired by https://www.youtube.com/watch?v=CQFnD5ddRFc
## But I thought I could do it better so here we are

## Goals for THRESHER

## BASIC CAPABILITIES
## Call and response system with STT and TTS capabilities                                   STT ✅ TTS ❌
## OBS integration, for "Clipping that S***"                                                ✅
## Opening and searching google within the default browser                                  ✅
## Basic calculations (addition, subtraction, multiplication, division, and percentages)    ❌
## Typing in Rivals chat, being able to work out which chat it's in                         Chat ✅ Smart Chat ❌
## Skipping songs, playing and pausing                                                      ✅
## some miscellaneous commands like pinging a website, coin flipping                        ✅
## sit in system tray and not bother me by being on the taskbar                             ✅

## POTENTIAL FUTURE CAPABILITIES:
## Being able say what song is playing (Integration with Trixinous/CiderSongMonitor)
## Discord integration? (being able to message for me, etc.)
## Opening games and programs
## More advanced calculations (ratios expressed as whole numbers)



## STT and TTS will be in:          THRESHER                .py
## Command Parsing will be in:      THRESHER                .py
## OBS Integration will be in:      THRESHER_OBS_INTEG      .py
## Google Search will be in:        THRESHER_GOOGLE_SEARCH  .py
## Hardware Monitoring will be in:  THRESHER_HW_MONITOR     .py
## Inbuilt Calculator will be in:   THRESHER_CALCULATOR     .py
## Marvel Rivals Chat will be in:   THRESHER_RIVALS_CHAT    .py
## Media Control will be in:        THRESHER_MEDIA_CONTROL  .py
## Miscellaneous stuff will be in:  THRESHER_MISCELLANEOUS  .py

## THRESHER's modules are stored within /THRESHER/lib

# Import THRESHER modules
from lib import THRESHER_GOOGLE_SEARCH as google_search_module
from lib import THRESHER_HW_MONITOR    as hw_monitor_module             # Currently not possible to measure temps on Windows using Python without access to a service like OpenHWMonitor. As such temperature commands will return nothing on windows
from lib import THRESHER_OBS_INTEG     as obs_integ_module
from lib import THRESHER_CALCULATOR    as calculator_module
from lib import THRESHER_RIVALS_CHAT   as marvel_rivals_chat_module
from lib import THRESHER_MEDIA_CONTROL as media_control_module
from lib import THRESHER_MISCELLANEOUS as miscellaneous_module

# Import external modules
import winsound
import speech_recognition as sr
import asyncio
import ctypes
import tkinter as tk
import pystray
import threading
import time
import subprocess
import os
import sys
import winreg
import json
from PIL import Image


speech_recognition_running = True
current_icon_state = "THRESHER"


## The default config. saved to HKEY_CURRENT_USER\Software\Trixinous\THRESHER in the Registry.
DEFAULT_CONFIG = {
    "obs_token": "",
    "wake_words": ["thresher", "thresh", "thrash", "thrasher"],
    "THRESHER_version": "20250224-2"
    "THRESHER_internal_version: 1" # Does not correspond to the actual update, is just incremented whenever the version is updated - Used to check whether new things need to be written to the Registry.
}


## Command Tuple Library - This is the group of tuples for commands
google_commands = ("google", "show me", "convert", "search", "who", "whom", "whose", "what", "why", "when", "where", "are", "how")
hw_monitor_commands = ()
OBS_commands = ("clip that", "clip", "start recording", "stop recording")
calculator_commands = ()
marvel_rivals_commands = ("type in chat", "type and chat", "type in rivals", "type and rivals", "type in team", "type and team", "type in faction", "type and faction", "type in match", "type and match")
media_commands = ("play", "pause", "stop", "skip", "next track", "previous", "last track" )
miscellaneous_commands = ("flip a coin", "coinflip", "heads or tails", "start a connection test", "speed test" "start a speed test", "show thresher window")


class TextRedirector(object):  # Custom stdout object
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.insert(tk.END, str)
        self.text_widget.see(tk.END)  # Scroll to the end

    def flush(self):  # For compatibility with some streams
        pass

def recognised_commands(passed_command):
    print("A command has been passed to the recognised_commands list. Checking:")
    '''
    Google Commands. 
    Recognises phrases like "google", "show me", "convert", "search" "who", "whom, whose, what, why, when, where, are and how and passes it to google_search_module
    '''
 
    if any(passed_command.lower().startswith(word) for word in google_commands):
        print("Command recognised as Google command! Searching Google...")
        google_search_module.perform_google_search(True, passed_command)
    
    '''
    Hardware Monitoring Commands. 
    Recognises phrases like "system temp", "system specs", "cpu temp", "cpu load", "gpu temp", "gpu load", "task manager"
    '''
    
    '''
    OBS Commands. 
    Recognises phrases like "clip that", "clip", "start recording", "stop recording"
    '''

    if any(word in passed_command for word in OBS_commands):
        print("Command recognised as OBS command!")
        if "clip that" in passed_command or "clip" in passed_command:
            obs_integ_module.obs_integration("clip that")
        elif "start recording" in passed_command:
            obs_integ_module.obs_integration("start recording")
        elif "stop recording" in passed_command:
            obs_integ_module.obs_integration("stop recording")

    '''
    Calculator Commands.
    Recognises phrases like "+", "-" "x" "/", "in bin" "in binary", "in hex", "in hexadecimal" "as a ratio*"
    *(struggles to recognise my Cumbrian accent with the word "ratio" so I may have to rethink that one, maybe a math input panel?)
    '''

    '''
    Marvel Rivals Commands.
    '''

    if any(word in passed_command for word in marvel_rivals_commands):
        print("Command recognised as Marvel Rivals Chat command!")
        if "type in chat" in passed_command or "type in rivals" in passed_command  or "type and chat" in passed_command or "type and rivals" in passed_command:
            marvel_rivals_chat_module.chat("generic", passed_command)
        elif "type in team" in passed_command or "type and team" in passed_command:
            marvel_rivals_chat_module.chat("team", passed_command)
        elif "type in faction" in passed_command or "type and faction" in passed_command:
            marvel_rivals_chat_module.chat("faction", passed_command)
        elif "type in match" in passed_command or "type and faction" in passed_command:
            marvel_rivals_chat_module.chat("match", passed_command)

    '''
    Media Commands.
    '''

    if any(word in passed_command for word in media_commands):
        print("Command recognised as a media command!")
        if passed_command == "play":
            media_control_module.play_pause()
        elif passed_command == "pause" or passed_command == "stop":
            media_control_module.play_pause()
        elif passed_command == "skip" or passed_command == "next track":
            media_control_module.skip()
        elif passed_command == "previous" or passed_command == "last track":
            media_control_module.previous()
   
    '''
    Miscellaneous Commands.
    '''

    if any(word in passed_command for word in miscellaneous_commands):
        print("Command recognised as a miscellaneous command!")
        if "flip a coin" in passed_command or "coinflip" in passed_command or "heads or tails" in passed_command:
            miscellaneous_module.coinflip()
        if "ping" in passed_command or "start a connection test" in passed_command:
            miscellaneous_module.ping()
        if "start a speed test" in passed_command or "speed test" in passed_command:
            miscellaneous_module.speedtest()
        if "show thresher window" in passed_command:
            on_click("THRESHER", "Show/Hide GUI")

def on_click(icon, item):
    if str(item) == "Exit":
        global speech_recognition_running
        speech_recognition_running = False  # Signal speech thread to stop

        icon.visible = False  # Hide the icon immediately
        icon.stop()  # Stop the icon's event loop

        root.withdraw()  # Hide the main window

        def _safe_exit():
            root.destroy()  # Destroy the Tkinter window (on main thread)
            sys.exit() # Force quit to kill lingering threads

        root.after(0, _safe_exit)  # Schedule on main thread

    elif str(item) == "Show/Hide GUI":
        global gui_visible
        if gui_visible:
            root.withdraw()
            gui_visible = False
        else:
            root.deiconify()
            gui_visible = True

def on_closing():  # Function to handle window close event
    global gui_visible
    root.withdraw()  # Hide the window (don't destroy it)
    gui_visible = False # Update the gui_visible variable

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

icon_images = {
    "THRESHER": Image.open(resource_path("res/img/ico/THRESHER.png")),  # Use resource_path!
    "accept": Image.open(resource_path("res/img/ico/THRESHER_accept.png")), # Use resource_path!
    "error": Image.open(resource_path("res/img/ico/THRESHER_error.png")), # Use resource_path!
    "listen": Image.open(resource_path("res/img/ico/THRESHER_listen.png")), # Use resource_path!
}

def print_output_to_gui():
    global text_area  # Make sure text_area is global so we can access it
    text_area.delete("1.0", tk.END)  # Clear previous output
    # ... (Your logic to generate the output you want to display) ...
    output_to_display = "This is the output from your function.\n"  # Example
    output_to_display += "More output can go here.\n"  # Example
    # ... (More logic to generate output)

    text_area.insert(tk.END, output_to_display)  # Insert the output into the text area

def setup_gui():
    global root, text_area, stdout_redirector
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.title("THRESHER CLI")
    # ... (other Tkinter setup)
    root.withdraw()  # Hide the main window initially
    # Create a Text widget to display output
    text_area = tk.Text(root, wrap=tk.WORD)  # wrap=tk.WORD for line wrapping
    text_area.pack(expand=True, fill=tk.BOTH) # Make it expand to fill window

    stdout_redirector = TextRedirector(text_area)  # Create redirector
    import sys
    sys.stdout = stdout_redirector  # Redirect stdout

def setup_icon():
    image_path = resource_path("res/img/ico/THRESHER.png")
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: Icon image not found at {image_path}")
        return None, None

    menu = pystray.Menu(
        pystray.MenuItem("Show/Hide GUI", on_click),  # Toggle GUI visibility
        pystray.MenuItem("Exit", on_click),
    )

    icon = pystray.Icon("THRESHER", image, "THRESHER", menu)
    return icon # Return the icon

def run_icon(icon):
    icon.run()

def update_icon(icon, state):
    global current_icon_state # Access global icon
    if state != current_icon_state:  # Only update if the state has changed
        current_icon_state = state
        icon.icon = icon_images[state]  # Update the icon image
        icon.update_menu()  # Refresh the menu (sometimes needed)

        if state in ("accept", "error"):
            timer = threading.Timer(5, update_icon, args=(icon, "THRESHER"))  # 0.5s delay
            timer.start()
        elif state == "listen":  # Start timer immediately for "listen"
            timer = threading.Timer(0, update_icon, args=(icon, "listen"))  # 0s delay
            timer.start()

def save_config_to_registry(config):
    try:
        key_path = r"Software\Trixinous\THRESHER"  # Modified registry path
        key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        for setting, value in config.items():
            if isinstance(value, list) or isinstance(value, dict):  # Handle lists/dicts
                winreg.SetValueEx(key, setting, 0, winreg.REG_SZ, json.dumps(value))  # Store as JSON string
            elif isinstance(value, bool): # handle boolean types
                winreg.SetValueEx(key, setting, 0, winreg.REG_SZ, str(value))
            else:
                winreg.SetValueEx(key, setting, 0, winreg.REG_SZ, str(value))  # Convert to string
        winreg.CloseKey(key)
        print("Config saved to registry.")
    except Exception as e:
        print(f"Error saving config to registry: {e}")

def load_config_from_registry():
    try:
        key_path = r"Software\Trixinous\THRESHER"  # Modified registry path
        key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        config = {}
        i = 0
        while True:
            try:
                name, value, type = winreg.EnumValue(key, i)
                if type == winreg.REG_SZ:
                    try:
                        config[name] = json.loads(value)  # Try to parse JSON (for lists/dicts)
                    except json.JSONDecodeError:
                        if value.lower() == "true":
                            config[name] = True
                        elif value.lower() == "false":
                            config[name] = False
                        else:
                            config[name] = value  # If not JSON, keep as string
                i += 1
            except OSError:  # Reached end of values
                break
        winreg.CloseKey(key)
        print("Config loaded from registry.")
        return config
    except FileNotFoundError:
        print("Config not found in registry. Creating default config in registry.")
        save_config_to_registry(DEFAULT_CONFIG)  # Create default config in registry
        return DEFAULT_CONFIG
    except Exception as e:
        print(f"Error loading config from registry: {e}")
        return DEFAULT_CONFIG



def speech_to_text(icon):
    global speech_recognition_running
    recogniser = sr.Recognizer()
    config = load_config_from_registry()
    wake_words = config["wake_words"]
    max_attempts = 10
    attempts_before_error_icon = 10 # Number of attempts before showing the error icon


    while speech_recognition_running:
        attempt = 0
        try:
            with sr.Microphone() as source:
                recogniser.adjust_for_ambient_noise(source)
                print("Microphone connected. Listening for THRESHER input...")
                update_icon(icon, "THRESHER")  # Reset icon

                while speech_recognition_running: # inner loop
                    try:
                        audio = recogniser.listen(source, timeout=5, phrase_time_limit=7)
                        text = recogniser.recognize_google(audio).lower()
                        print(f"Heard: {text}")

                        if any(word in text for word in wake_words):
                            print("Wake word detected!")
                            update_icon(icon, "listen")
                            winsound.Beep(1000, 60)
                            winsound.Beep(1200, 80)

                            print("Listening for command...")
                            try:
                                audio = recogniser.listen(source)  # No timeout for command
                                command = recogniser.recognize_google(audio).lower()
                                print(f"Command: {command}")
                                recognised_commands(command)
                                update_icon(icon, "accept")
                                winsound.Beep(1200, 80)
                                winsound.Beep(1000, 60)

                            except sr.UnknownValueError:
                                update_icon(icon, "error")
                                print("Sorry, I couldn't understand what you said.")
                                winsound.Beep(400, 80)
                                winsound.Beep(400, 80)
                                winsound.Beep(400, 80)

                            update_icon(icon, "THRESHER")

                    except sr.WaitTimeoutError:
                        pass # Just continue listening in the background
                    except sr.UnknownValueError:
                        pass # Just continue listening in the background
                    except sr.RequestError as e:
                        print(f"Speech recognition request error: {e}")
                        update_icon(icon, "error") # Show error icon
                        time.sleep(5)
                        break # Break out of inner loop to retry microphone connection
                    if not speech_recognition_running:
                        break # Exit inner loop if speech recognition is stopped

        except OSError as e:
            attempt += 1
            print(f"Microphone not ready: {e}. Retrying in 1 second (Attempt {attempt})...")
            if attempt >= attempts_before_error_icon:
                update_icon(icon, "error")  # Show error icon AFTER a certain number of attempts
            time.sleep(1)  # Wait before retrying
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            update_icon(icon, "error")
            speech_recognition_running = False
            return
        
def text_to_speech():
    return

def main_function():
    global root, terminal_visible, console_window_handle, gui_visible, icon_thread, speech_thread, icon
    
    gui_visible = False
    terminal_visible = False  # Initialize terminal visibility flag
    root = tk.Tk()  # Tkinter root window
    root.title("THRESHER CLI")
    ctypes.windll.kernel32.SetConsoleTitleW("THRESHER CLI")
    root.withdraw()  # Hide the main window initially

    # Get the console window handle (for showing/hiding)
    #console_window_handle = ctypes.windll.kernel32.GetConsoleWindow()
    #if console_window_handle != 0: # Check if a console exists
        #print("Console window handle found.")
    #else:
        #print("No console window found.")
        # If running from a GUI shortcut without a console, you might want to create one
        # subprocess.Popen(['cmd.exe']) # This will open a new command prompt.
        # console_window_handle = ctypes.windll.kernel32.GetConsoleWindow() # You might need a delay here.

    icon = setup_icon()

    if icon is None:  # Handle the case where the icon setup failed
        print("Icon setup failed. Exiting.")
        return  # or handle it differently

    icon_thread = threading.Thread(target=run_icon, args=(icon,))
    icon_thread.daemon = True  # Important: Set daemon to True
    icon_thread.start()


    # Start speech recognition in a separate thread
    speech_thread = threading.Thread(target=speech_to_text, args=(icon,))
    speech_thread.daemon = True  # Important: Set daemon to True
    speech_thread.start()

    setup_gui() # Setup the GUI

    root.mainloop()

if __name__ == "__main__":
    main_function()
