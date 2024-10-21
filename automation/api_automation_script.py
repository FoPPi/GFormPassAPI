import requests
import schedule
import time
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# API configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://api-app:8000')
ADMIN_KEY = os.getenv('ADMIN_KEY')


def call_api_endpoint(endpoint):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"X-Admin-Key": ADMIN_KEY}

    try:
        response = requests.delete(url, headers=headers) if endpoint == "/question" else requests.patch(url,
                                                                                                        headers=headers)
        response.raise_for_status()
        logger.info(f"Successfully called {endpoint}: {response.json()}")
    except requests.RequestException as e:
        logger.error(f"Error calling {endpoint}: {str(e)}")


def delete_questions():
    call_api_endpoint("/question")


def update_user_keys():
    call_api_endpoint("/user/update_keys")


def run_scheduled_jobs():
    schedule.every().day.at("00:00").do(delete_questions)
    schedule.every().day.at("00:05").do(update_user_keys)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for 60 seconds before checking again


if __name__ == "__main__":
    logger.info("Starting API automation script")
    run_scheduled_jobs()