from fastapi import FastAPI
from app.api.llm import router as llm_router
from app.db.init_db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()
app.include_router(llm_router)
