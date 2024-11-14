import datetime
import logging
import requests
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    
    # Define the URL you want to check
    url = "https://example.com"
    
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()
        
        # Log the status code and content for debugging
        logging.info(f"Website checked at {utc_timestamp}")
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Content: {response.text[:100]}")  # Logs first 100 chars
        
    except requests.RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
    
    if mytimer.past_due:
        logging.warning("The timer is past due!")

    logging.info("Timer trigger function ran successfully.")
