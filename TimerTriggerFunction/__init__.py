import requests
import logging
import mysql.connector
from urllib.parse import urlparse

# Connection string
connection_string = "mysql://your-database-user:your-database-password@your-database-host/your-database-name"

def parse_connection_string(conn_string):
    parsed = urlparse(conn_string)
    return {
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port or 3306,  # Default MySQL port
        'database': parsed.path.lstrip('/')
    }

db_config = parse_connection_string(connection_string)

def update_opportunity_and_check(id, opportunity_stage_id):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Check if the record exists
        cursor.execute("SELECT * FROM apollo_opportunities WHERE id = %s", (id,))
        rows = cursor.fetchall()

        if not rows:
            logging.info(f"No record found with id: {id}")
            return

        current_stage_id = rows[0]['opportunity_stage_id']

        # Check the specific condition
        if current_stage_id == '657c6cc9ab96200302cbd0a3' and opportunity_stage_id == '669141aa1bcf2c04935c3074':
            logging.info("Condition met, setting has_changed to true...")
            # Update `has_changed` to true
            cursor.execute(
                "UPDATE apollo_opportunities SET has_changed = %s WHERE id = %s",
                (True, id)
            )

        # Update the stage ID
        cursor.execute(
            "UPDATE apollo_opportunities SET opportunity_stage_id = %s WHERE id = %s",
            (opportunity_stage_id, id)
        )

        connection.commit()
        logging.info(f"Record updated: id={id}, opportunity_stage_id={opportunity_stage_id}")

    except mysql.connector.Error as err:
        logging.error(f"Error in update_opportunity_and_check: {err}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_and_process_deals(api_key, sort_by_field='amount', per_page=100):
    base_url = 'https://api.apollo.io/api/v1/opportunities/search'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'X-Api-Key': api_key
    }

    current_page = 1

    try:
        while True:
            url = f"{base_url}?sort_by_field={sort_by_field}&page={current_page}&per_page={per_page}"
            logging.info(f"Fetching page {current_page} with up to {per_page} results...")

            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Error: {response.status_code} - {response.reason}")

            data = response.json()
            opportunities = data.get('opportunities', [])
            pagination = data.get('pagination', {})

            logging.info(f"Page {current_page} retrieved. Total deals returned on this page: {len(opportunities)}")

            # Filter deals by `opportunity_stage_id`, excluding null values
            filtered_deals = [
                deal for deal in opportunities
                if deal.get('opportunity_stage_id') == "657c6cc9ab96200302cbd0a3"
            ]

            # Process each deal by passing its data to `update_opportunity_and_check`
            for deal in filtered_deals:
                id = deal.get('id')
                opportunity_stage_id = deal.get('opportunity_stage_id')

                try:
                    update_opportunity_and_check(id, opportunity_stage_id)
                    logging.info(f"Processed deal with ID: {id}, Opportunity Stage ID: {opportunity_stage_id}")
                except Exception as error:
                    logging.error(f"Error processing deal with ID: {id}", error)

            logging.info(f"Filtered deals processed from page {current_page}: {len(filtered_deals)}")

            # Check pagination
            if pagination.get('has_next_page'):
                current_page += 1
            else:
                logging.info('No more pages to fetch. Exiting loop.')
                break

        logging.info('All pages processed successfully.')
    except Exception as error:
        logging.error('Error fetching and processing deals:', error)
        raise

# Example usage:
# api_key = "your-api-key-here"
# fetch_and_process_deals(api_key)
