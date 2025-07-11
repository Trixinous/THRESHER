
# "https://www.google.com/search?q=thresher+sharks" <-- Example search

import webbrowser
import requests
import json

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

def format_name_for_wiki_search(THRESHER_granted_access, THRESHER_passed_command):
    if THRESHER_granted_access:
        # No input() call here, as THRESHER_passed_command is already passed
        # This function should just process the string it receives.
        parsed_command = THRESHER_passed_command.strip()

        if parsed_command.lower().startswith("who is"):
            parsed_command = parsed_command[len("who is"):].strip()
        elif parsed_command.lower().startswith("whom is"):
            parsed_command = parsed_command[len("whom is"):].strip()
        elif parsed_command.lower().startswith("who"):
            parsed_command = parsed_command[len("who"):].strip()
        elif parsed_command.lower().startswith("whom"):
            parsed_command = parsed_command[len("whom"):].strip()

        if parsed_command: # Ensure input is not empty after stripping
            proper_cased_name = parsed_command.title()
            return proper_cased_name
        else:
            return "usrerror"
    else:
        return "usrerror" # Or handle the case where access is not granted appropriately

def perform_wiki_search(THRESHER_granted_access, person_name, num_sentences):
    """
    Fetches a brief description of a famous person from Wikipedia.

    Args:
        THRESHER_granted_access (bool): Whether access is granted.
        person_name (str): The name of the famous person (e.g., "Albert Einstein").
        num_sentences (int): The number of sentences to retrieve for the description.

    Returns:
        tuple: A tuple containing (str: description, str: person_name, int: num_sentences)
               or (str: error message, None, None) if an error occurs or not found.
    """
    if not THRESHER_granted_access:
        return "Access not granted to perform Wikipedia search.", None, None

    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exsentences": num_sentences,
        "explaintext": 1,
        "titles": person_name,
        "format": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        pages = data.get('query', {}).get('pages', {})

        for page_id, page_data in pages.items():
            if page_id == '-1':
                return None, None
            else:
                extract = page_data.get('extract')
                if extract:
                    return extract, person_name
                else:
                    return None, None
        return None, None

    except requests.exceptions.RequestException as e:
        return f"An error occurred during the request: {e}", None, None
    except json.JSONDecodeError:
        return "Failed to decode JSON response from Wikipedia API.", None, None