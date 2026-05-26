from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware 
from db import connect_db, disconnect_db , pool

app = FastAPI()

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


@app.on_event("startup")
async def startup_event():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_db()   

@app.get("/")
async def home():
    return FileResponse("templates/index.html")


@app.post("/api/contact")
async def contact(data: ContactMessage):

    await pool.execute(
        "INSERT INTO contact_messages (name, phone, message) VALUES ($1, $2, $3)",
        data.name, data.phone, data.message
    )

    return JSONResponse({
        "success": True,
        "message_ar": "تم استلام رسالتك",
        "message_fr": "Message reçu"
    })


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)