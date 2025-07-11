import random
import ping3
import webbrowser
import sys
import os
#from lib import THRESHER_TOAST_W10T_P as ToastModule
from windows_toasts import Toast, WindowsToaster, ToastDisplayImage
#from win10toast_persist import ToastNotifier



try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")

T_icon_path = os.path.join(base_path, "res", "img", "ico", "THRESHER_128.png")

print(f"Attempting to load icon from: {T_icon_path}") # debugstring

# winotify, handles Windows Toasts
def show_winotify_toast(title, message):
   # toaster = ToastModule.ToastNotifier()
   # toaster.show_toast(
   #     title,
   #     message,
   #     icon_path= T_icon_path,
   #     duration=None,
   #     threaded=True,
   # )
    toaster = WindowsToaster("Trixinous.App.THRESHER")
    newToast = Toast()
    newToast.text_fields = [title, message]
    newToast.AddImage(ToastDisplayImage.fromPath(T_icon_path))
    toaster.show_toast(newToast)
    


## The Coinflip Function
def coinflip():
    result = random.randrange(1,100)
    if result < 50:
        print("Heads")
        show_winotify_toast("Coin Flip", "Coin Flip returned Heads")
    elif result >= 51:
        print("Tails")
        show_winotify_toast("Coin Flip", "Coin Flip returned Tails")

## The Ping Function
def ping():
    pinged_sites = 0
    hostnames = ("google.com", "twitter.com", "twitch.tv", "github.com", "192.168.1.254")
    for x in hostnames:
        try:
            delay = ping3.ping(x)  # Returns delay in seconds or None if failed
            if delay is not None:
                print(f"{x} is reachable. Delay: {delay:.4f} seconds")  # Format delay
                pinged_sites = pinged_sites + 1
            else:
                print(f"{x} is unreachable.")
        except Exception as e:
            print(f"An error occurred: {e}")  # Handle potential exceptions
            return False 
        if x == hostnames[-1]: # if the currently accessed hostname is the same as the last:
            print(f"Connection test concluded. {pinged_sites}/{len(hostnames)} sites successfully pinged.")

## The Speedtest Function - uses fast.com
def speedtest():
    webbrowser.open_new_tab("https://fast.com/")