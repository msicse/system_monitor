import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

# Mail server configurations
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.example.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', 'user@example.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'password')

# Screenshot directory (default to relative path for cross-platform compatibility)
SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR', 'data/screenshots')

# Data directory for storing reports and logs
DATA_DIR = os.getenv('DATA_DIR', 'data')

# CVE API configurations
CVE_API_BASE_URL = os.getenv('CVE_API_BASE_URL', 'https://cve.circl.lu/api')
CVE_REQUEST_TIMEOUT = int(os.getenv('CVE_REQUEST_TIMEOUT', 10))
CVE_MAX_RESULTS = int(os.getenv('CVE_MAX_RESULTS', 50))