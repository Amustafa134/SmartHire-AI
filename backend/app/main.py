from fastapi import FastAPI
#from routes import cv_routes, job_routes, match_routes, interview_routes

app = FastAPI(title="SmartHire AI - MVP")

#app.include_router(cv_routes.router)
#app.include_router(job_routes.router)
#app.include_router(match_routes.router)
#app.include_router(interview_routes.router)

@app.get("/Welcome")
def root():
    return {
        "message": "SmartHire AI backend is running"
    }