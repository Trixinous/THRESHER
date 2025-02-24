import random
import ping3
import webbrowser

## The Coinflip Function
def coinflip():
    result = random.randrange(1,100)
    if result < 50:
        print("Heads")
    elif result >= 51:
        print("Tails")

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