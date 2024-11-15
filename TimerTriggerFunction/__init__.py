import logging
import requests

def main(mytimer):
    logging.info("Timer trigger function started.")
    try:
        response = requests.get("https://catfact.ninja/fact")
        logging.info(f"Cat Fact: {response}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise  # Re-raise the error to propagate it to Azure logs
    logging.info("Timer trigger function completed successfully.")
