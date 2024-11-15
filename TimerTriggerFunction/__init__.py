import logging
import azure.functions as func
import requests

def main(mytimer: func.TimerRequest) -> None:
    # Log "Hello World" each time the function is triggered
    logging.info("Hello World")

    # Optional: Log if the timer is past due
    if mytimer.past_due:
        logging.warning("The timer is past due!")

    # Make an HTTP GET request to catfact.ninja/fact
    try:
        response = requests.get("https://catfact.ninja/fact")
        response.raise_for_status()  # Raise an error for HTTP error responses (4xx/5xx)
        fact = response.json().get("fact", "No fact found")
        logging.info(f"Cat Fact: {fact}")
    except requests.RequestException as e:
        logging.error(f"Failed to fetch cat fact: {e}")

    # Log a message indicating the function ran successfully
    logging.info("Timer trigger function ran successfully.")
