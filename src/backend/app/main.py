from fastapi import FastAPI
from backend.app.routes import base, data


app = FastAPI(title="SmartHire AI - MVP")

app.include_router(base.base_router)
app.include_router(data.data_router)
