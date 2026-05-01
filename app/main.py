from fastapi import FastAPI
from app.api.llm import router as llm_router

app = FastAPI()

app.include_router(llm_router)