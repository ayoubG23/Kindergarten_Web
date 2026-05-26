# -----------------------------------------------------------
# PostgreSQL raw connection test
# -----------------------------------------------------------

import asyncpg
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Global connection pool variable
pool=None
async def connect_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)

async def disconnect_db():
    global pool
    if pool:
        await pool.close()

