from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware 
import db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    await db.connect_db()
    yield
    await db.disconnect_db()


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


class ContactMessage(BaseModel):
    name: str
    phone: str
    message: str



@app.get("/")
async def home():
    return FileResponse("templates/index.html")


@app.post("/api/contact")
async def recieveMsg(msg:ContactMessage):
    query=""" INSERT INTO contact_messages (name,phone,message) VALUES ($1,$2,$3) """
    async with db.pool.acquire() as conn:
        await conn.execute(query,msg.name,msg.phone,msg.message)
    return JSONResponse({
        "success": True,
        "message_ar": "تم استلام رسالتك",
        "message_fr": "Message reçu"
    })

#for local test
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)