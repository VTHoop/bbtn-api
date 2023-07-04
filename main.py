from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router

config = dotenv_values(".env")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient("localhost", 27017)
    app.database = app.mongodb_client["bbtn"]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(router, tags=["games"], prefix="/games")
