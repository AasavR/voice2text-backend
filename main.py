from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from auth import router as auth_router
#from wallet import router as wallet_router
from transcribe import router as transcribe_router

from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
from vosk import Model

model = Model("model/vosk-model-small-hi-0.22")


app = FastAPI()

class FormatRequest(BaseModel):
    field1: str
    field2: int

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from temp_audio directory
temp_audio_path = os.path.join(os.path.dirname(__file__), "temp_audio")
app.mount("/temp_audio", StaticFiles(directory=temp_audio_path), name="temp_audio")

#app.include_router(auth_router, prefix="/auth")
#app.include_router(wallet_router, prefix="/wallet")
app.include_router(transcribe_router, prefix="/transcribe")
from .templates import router as templates_router
app.include_router(templates_router, prefix="/templates")

@app.get("/")
def read_root():
    return {"message": "Voice2Text API Running"}

    

# Remove the placeholder /templates/format endpoint to avoid conflict with templates router

# @app.post("/templates/format")
# async def format_template(request: FormatRequest):
#     return {"message": "Success", "data": request.dict()}
