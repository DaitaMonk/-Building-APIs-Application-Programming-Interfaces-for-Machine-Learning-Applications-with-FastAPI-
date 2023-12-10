from typing import Union, List, Literal
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pandas as pd
import joblib
import os
import numpy as np
from sklearn.preprocessing import FunctionTransformer

# loading machine learning component
def load_ml_components(ml):
    "load the ml components to re-use in app"
    with open(ml, "rb") as fold:
        object = joblib.load(fold)
    return object

# Instantiating the FastAPI method
app = FastAPI()

# specifying the datatypes of each column in the model 
class Sepsis(BaseModel):
    PRG: float
    PL: float
    SK: float
    TS: float
    M11: float
    BD2: float
    Age: float
    
# Loading the model
model = joblib.load('dev/best_model.joblib')

# @app.get("/"): This is a FastAPI decorator 
# that defines a route for handling HTTP GET requests to the root ("/") endpoint.
@app.get("/")

# Defines an asynchronous function named root
async def root():
    return {
        "info": "Sepsis Classification API : Ths is my api floaterface"
    }

# Returns a JSON response with information about the 
# API when a GET request is made to the root endpoint.
@app.post("/classify")
async def sepsis_classification(Sepsis: Sepsis):
    try:
        # create data frame
        df = pd.DataFrame({
            "PRG": [Sepsis.PRG],
            "PL": [Sepsis.PL],
            "SK": [Sepsis.SK],
            "TS": [Sepsis.TS],
            "M11": [Sepsis.M11],
            "BD2": [Sepsis.BD2],
            "Age": [Sepsis.Age]
        }

        )
        # output prediction
        output = model.predict(df)
        print(
            f"The data has been classified"
        )
        msg = "Execution went Fine"
        code = 1
        if output == 0:
            Sepsis = "Negative"
        else:
            Sepsis = "Positive"

    except:
        print(
            f"Something went wrong during the Sepssis calssification"
        )
        msg = "Execution went wrong"
        code = 1
        Sepsis = None
    result = {"execution_message": msg,
              "execution_code": code, "prediction": Sepsis}
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
