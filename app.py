from flask import Flask
from src.db.connect import get_mysql
import logging

app = Flask(__name__)

if __name__ == '__main__':
    # connect to db
    mysql = get_mysql()

    # Configure the logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Connect to the database
    try:
        mysql.connection.ping()
        logging.info("Connected to the database successfully")
    except Exception as e:
        logging.error("Failed to connect to the database: %s", str(e))

    # Change the port to 5006
    app.run(host='0.0.0.0', port=5006)
