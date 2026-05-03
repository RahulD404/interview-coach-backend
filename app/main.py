from fastapi import FastAPI

from app.api.llm import router as llm_router
from app.api.upload import router as upload_router
from app.api.questions import router as questions_router

from app.db.init_db import init_db

# ✅ Create app FIRST
app = FastAPI()


# ✅ Startup event
@app.on_event("startup")
def on_startup():
    init_db()


# ✅ Register routers
app.include_router(llm_router)
app.include_router(upload_router)
app.include_router(questions_router)