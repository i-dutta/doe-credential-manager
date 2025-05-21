# app/config.py

import os

# Get absolute path to the root project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
DATA_FILE = os.path.join(BASE_DIR, "data", "url_credentials.csv")
KEY_FILE = os.path.join(BASE_DIR, "data", "secret.key")

# Environment options
ENV_OPTIONS = ["TEST", "PRE", "PSUP", "PROD"]

# CSV expected columns
CSV_COLUMNS = ["Environment", "Application", "URL", "Username", "Password"]

# Streamlit session state keys
FORM_ENV = "form_env"
FORM_SYSTEM = "form_system"
FORM_URL = "form_url"
FORM_USERNAME = "form_username"
FORM_PASSWORD = "form_password"
EDIT_INDEX = "edit_index"
PENDING_DELETE = "pending_delete"
FORM_KEY = "form_key"
UPLOAD_SUCCESS_MESSAGE_KEY = "upload_success_message"
URL_DATA_KEY = "url_data"
