import logging
import azure.functions as func

def main(mytimer: func.TimerRequest) -> None:
    # Log "Hello World" each time the function is triggered
    logging.info("Hello World")

    # Optional: Log if the timer is past due
    if mytimer.past_due:
        logging.warning("The timer is past due!")

    # Log a message indicating the function ran successfully
    logging.info("Timer trigger function ran successfully.")
