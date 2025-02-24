import time
import ctypes
import keyboard 

# Define media keycodes
VK_MEDIA_PLAY_PAUSE = 0xB3      # Example: Media Play/Pause key
VK_MEDIA_NEXT_TRACK = 0xB0      # Example: Media Next Track key
VK_MEDIA_PREVIOUS_TRACK = 0xB1  # Example: Media Previous Track
VK_MEDIA_STOP = 0xB2            # Example: Media Stop

# Send a key press and release event
def send_key(keycode):
    ctypes.windll.user32.keybd_event(keycode, 0, 0, 0)  # Key press
    ctypes.windll.user32.keybd_event(keycode, 0, 0x8000, 0)  # Key release

def play_pause():
    send_key(VK_MEDIA_PLAY_PAUSE)
    print("Play/Pause pressed")

def skip():
    send_key(VK_MEDIA_NEXT_TRACK)
    print("Skip pressed")

def previous():
    send_key(VK_MEDIA_PREVIOUS_TRACK)
    print("Previous pressed")





