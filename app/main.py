import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    chefbot_router,
)

app = FastAPI()

app.include_router(chefbot_router.router)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Welcome"])
def welcome():
    return "Welcome miss Nehal. I am Chef Bot"


if __name__ == "__main__":
    uvicorn.run(app=app, host="100.118.93.100", port=6969)
