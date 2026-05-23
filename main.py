from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


class ContactMessage(BaseModel):
    name: str
    phone: str
    message: str


@app.get("/")
async def home():
    return FileResponse("templates/index.html")


@app.post("/api/contact")
async def contact(data: ContactMessage):

    print(f"{data.name} | {data.phone} | {data.message}")

    return JSONResponse({
        "success": True,
        "message_ar": "تم استلام رسالتك",
        "message_fr": "Message reçu"
    })


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)