"""
This file includes the API requests and their configurations, along with
the configuration of the requests and responses.
"""

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import pickle
import numpy as np
from app.db import SessionLocal, get_db,\
 create_prediction_table, prediction_table_insert, select_id_repetition
np.set_printoptions(suppress=True)

app = FastAPI()

@app.on_event("startup")
def startup():
    session = SessionLocal()
    session.execute("select 1")
    """ Here we call the functions to create the prediction table.
    This functions are written in db.py """
    create_prediction_table()
    session.close()


class PredictRequest(BaseModel):
    id: int
    recency_7: int
    frequency_7: int
    monetary_7: float


class PredictResponse(BaseModel):
    id: int
    monetary_30: float


class CountResponse(BaseModel):
    id: int
    count: int


@app.get("/health", response_model=str)
async def get_health():
    """
    check for API health
    """
    return "API is healthy"

# In case of a post request, this function runs
@app.post("/api/predict", response_model=PredictResponse)
async def predict_monetary(request_payload: PredictRequest):
    """ Here I load the scaler used to scale the training set, to be used
    to scale the new input, and the trained ML Model """

    def load_saved_variables():
        path  = "/app/resources/"
        scaler = pickle.load(open(path + 'fitted_scaler.pkl', 'rb'))
        model = pickle.load(open(path + 'trained_model.pkl', 'rb'))
        return scaler, model

    """ Here I transform the features in the same way done when training
    the model. First transform the requency_7 feature to one-hot, 
    and then normalize the feature space """
    def preprocess_data(x_test):
        one_hot = np.zeros(7)
        one_hot[int(x_test[1])]=1
        x_test_one_hot = np.concatenate((x_test[2:], one_hot), axis = 0)
        x_test_scaled = scaler.transform(x_test_one_hot.reshape(1,-1))
        return x_test_scaled

    scaler, model = load_saved_variables()

    # Read the input from the request payload and then preprocess it.
    x_test = np.array(list(vars(request_payload).values()))
    x_test_scaled = preprocess_data(x_test)
    # Use the model to predict the output based on the processed input
    prediction = float(model.predict(x_test_scaled))
    
    """ Here we call the functions to insert the new prediction in 
    the table. This functions are written in db.py """
    create_prediction_table()
    prediction_table_insert(request_payload.id, prediction)

    return {'id': request_payload.id, 'monetary_30': prediction}

""" In case we want to get the number of prediction requests done for a 
specific passenger id, the get request runs this """
@app.get("/api/requests/{passenger_id}", response_model=CountResponse)
async def count_number_of_requests(
    passenger_id: int, sessions: Session = Depends(get_db)
):  
    # the method "select_id_repition" is written in db.py
    return {'id': passenger_id,\
     'count': int(select_id_repetition(passenger_id))}
