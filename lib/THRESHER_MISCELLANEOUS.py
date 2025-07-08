import random
import ping3
import webbrowser
import sys
import os
from win10toast import ToastNotifier
toast = ToastNotifier()


try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")

icon_path = os.path.join(base_path, "res", ".ico", "THRESHER.ico")

## The Coinflip Function
def coinflip():
    result = random.randrange(1,100)
    if result < 50:
        print("Heads")
        toast.show_toast(
            "Coin Flip",
            "Coin Flip returned Heads",
            duration = 20,
            icon_path = icon_path,
            threaded = True,
        )
    elif result >= 51:
        print("Tails")
        toast.show_toast(
            "Coin Flip",
            "Coin Flip returned Tails",
            duration = 20,
            icon_path = icon_path,
            threaded = True,
        )

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