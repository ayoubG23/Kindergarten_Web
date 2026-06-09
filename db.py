# -----------------------------------------------------------
# PostgreSQL raw connection test
# -----------------------------------------------------------

import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv('DATABASE_URL')
pool=None
if not DATABASE_URL:
    raise RuntimeError("no  DATABASE_URL found")
 
# Global connection pool variable
async def connect_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL,min_size=1,max_size=3)
    return pool

async def disconnect_db():
    await pool.close()
    

def getpool():
    if pool is None:
        raise RuntimeError("Data Base was not initialized")
    return pool


