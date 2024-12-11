import mysql.connector
import logging

# Connection string
connection_string = "mysql://your-database-user:your-database-password@your-database-host/your-database-name"

def parse_connection_string(conn_string):
    from urllib.parse import urlparse
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
