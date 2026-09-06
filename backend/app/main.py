from fastapi import FastAPI

from app.routers import health
from app.routers import auth


app = FastAPI()

app.include_router(health.router)
app.include_router(auth.router)