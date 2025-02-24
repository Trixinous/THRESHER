
# "https://www.google.com/search?q=thresher+sharks" <-- Example search

import webbrowser

THRESHER_granted_access = False  # Or True, depending on how it's passed
THRESHER_passed_command = ""  # Input passed from another script
ready_to_search = False
parsed_command = ""
search_query = ""

def perform_google_search(THRESHER_granted_access, THRESHER_passed_command):
    if THRESHER_granted_access:
        ## Strips "Google" from the command
        if "google" in THRESHER_passed_command.lower():
            parsed_command = THRESHER_passed_command.lower().replace("google", "", 1).strip()
        ## Strips "Search" or "Search for" from the command
        elif "search" in THRESHER_passed_command.lower():
            if "search for" in THRESHER_passed_command.lower():
                parsed_command = THRESHER_passed_command.lower().replace("search for", "", 1).strip()
            else:
                parsed_command = THRESHER_passed_command.lower().replace("search", "", 1).strip() 
        ## Continues if there's nothing to strip
        else:
            parsed_command = THRESHER_passed_command.lower().strip()

        search_query = parsed_command.replace(" ", "+")
        ready_to_search = True

    if ready_to_search:
        url = "https://www.google.com/search?q=" + search_query
        webbrowser.open(url)

        # Reset variables:
        THRESHER_granted_access = False
        THRESHER_passed_command = ""
        ready_to_search = False
        parsed_command = ""
        search_query = ""
