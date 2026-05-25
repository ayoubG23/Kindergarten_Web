# -----------------------------------------------------------
# PostgreSQL raw connection test
# -----------------------------------------------------------

import psycopg2
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Get PostgreSQL URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)

print("Connected successfully!")