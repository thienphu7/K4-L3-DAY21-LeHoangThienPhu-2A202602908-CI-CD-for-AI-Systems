from contextlib import asynccontextmanager
from pathlib import Path
import os
import joblib
import pandas as pd
from azure.storage.blob import BlobServiceClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

FEATURE_NAMES = ['age', 'workclass', 'education_num', 'marital_status', 'occupation',
                 'relationship', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week']
MODEL_KEY = 'artifacts/current/model.joblib'


def download_model():
    path = Path(os.environ.get('MODEL_PATH', '~/models/model.joblib')).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.download')
    with BlobServiceClient.from_connection_string(os.environ['AZURE_STORAGE_CONNECTION_STRING']) as client:
        blob = client.get_blob_client(os.environ['ARTIFACT_BUCKET'], MODEL_KEY)
        with temporary.open('wb') as stream:
            blob.download_blob().readinto(stream)
    temporary.replace(path)
    print('Model downloaded from Azure Blob Storage.', flush=True)
    return path


@asynccontextmanager
async def lifespan(app):
    app.state.model = joblib.load(download_model())
    yield


app = FastAPI(lifespan=lifespan)


class ScoreRequest(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)
    features: list[float]


@app.get('/healthz')
def healthz():
    return {'status': 'ok'}


@app.post('/score')
def score(req: ScoreRequest):
    if len(req.features) != 10:
        raise HTTPException(status_code=400, detail='Expected 10 features (adult income)')
    model = app.state.model
    features = pd.DataFrame([req.features], columns=FEATURE_NAMES)
    threshold = getattr(model, 'income_threshold_', None)
    if threshold is None:
        prediction = int(model.predict(features)[0])
    else:
        prediction = int(model.predict_proba(features)[0, 1] >= threshold)
    return {'prediction': prediction, 'label': 'thu_nhap_cao' if prediction == 1 else 'thu_nhap_thap'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
