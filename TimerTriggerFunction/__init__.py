import logging
import requests

def main(mytimer):
    logging.info("Timer trigger function started.")
    try:
        response = requests.get("https://catfact.ninja/fact")
        response.raise_for_status()
        fact = response.json().get("fact", "No fact found")
        logging.info(f"Cat Fact: {fact}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise  # Re-raise the error to propagate it to Azure logs
    logging.info("Timer trigger function completed successfully.")
