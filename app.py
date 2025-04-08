import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from network.exception.exception import CustomException
from network.logging.logger import logging
from network.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi import Form
import pandas as pd

from network.utils.main_utils.utils import load_object
from network.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from network.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from network.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["Homepage"])
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise CustomException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred

        # ✅ Optional tip starts here:
        df.columns = [col.replace('_', ' ').title() for col in df.columns]  # Make headers pretty
        df['Predicted Column'] = df['Predicted Column'].replace({1: "Phishing", 0: "Legit"})  # Rename values

        # Optional: Save predictions
        df.to_csv('prediction_output/output.csv', index=False)

        table_html = df.to_html(classes='table table-striped', index=False)

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise CustomException(e, sys)
    
@app.get("/manual_input")
async def manual_input_form(request: Request):
    return templates.TemplateResponse("manual_input.html", {"request": request})

@app.post("/manual_predict")
async def manual_input_predict(request: Request,
    has_ip: str = Form(...),
    long_url: str = Form(...),
    has_at_symbol: str = Form(...),
    has_redirect: str = Form(...),
    is_https: str = Form(...),
):
    try:
        # Map form values to numerical ones expected by model
        mapping = {"Yes": 1, "No": -1, "Neutral": 0}

        input_data = {
            "has_ip": mapping[has_ip],
            "long_url": mapping[long_url],
            "has_at_symbol": mapping[has_at_symbol],
            "has_redirect": mapping[has_redirect],
            "is_https": mapping[is_https]
        }

        df = pd.DataFrame([input_data])
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        prediction = network_model.predict(df)[0]

        result = "Legitimate" if prediction == 1 else "Phishing"
        return templates.TemplateResponse("manual_input.html", {
            "request": request,
            "result": result
        })

    except Exception as e:
        raise CustomException(e, sys)


    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)