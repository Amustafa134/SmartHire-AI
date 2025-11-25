from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.base import base_router
#from routes import base

load_dotenv(".env")


#from routes import cv_routes, job_routes, match_routes, interview_routes

app = FastAPI(title="SmartHire AI - MVP")


#app.include_router(cv_routes.router)
#app.include_router(job_routes.router)
#app.include_router(match_routes.router)
#app.include_router(interview_routes.router)

app.include_router(base_router)


# test_env.py
import os
from dotenv import load_dotenv

load_dotenv()

print("ENV:", os.getenv("YOUR_VARIABLE"))
