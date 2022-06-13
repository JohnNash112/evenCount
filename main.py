from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
from scoreModel import *

app = FastAPI()

class Cord(BaseModel):
    time: str
    Latitude: str
    Longitude: str
    speed: Optional[str] = ...
    
# class JsonList(BaseModel):
#     data: List[Cord]

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return("Hello there!, I am up:)")

@app.post("/getScore")
def score_fetch(dataRec:List[Cord]):
    collected_data = []
    for item in dataRec:
        collected_data.append([item.time, item.Latitude, item.Longitude, item.speed])
    print(collected_data)
    df = pd.DataFrame(collected_data, columns =['time', 'Latitude', 'Longitude', 'speed'])
    df["TripID"] = 'T-0'
    df['time'] = pd.to_numeric(df['time'], errors = 'ignore')
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors ='ignore')
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors ='ignore')
    df["speed"] = pd.to_numeric(df["speed"], errors ='ignore')
    print(df)
    dataGot = scoreValue(df)
    return{"Harsh Acceleration": dataGot['Harsh Acceleration'],
    'Harsh Braking': dataGot['Harsh Braking'],
    'Harsh Turn': dataGot['Harsh Turn'],
    'Normal': dataGot['Normal']}
