from pathlib import Path
from unittest.mock import MagicMock

import joblib
import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient
from sklearn.dummy import DummyClassifier
from src import serve


@pytest.fixture
def client(tmp_path, monkeypatch):
    model = DummyClassifier(strategy='constant', constant=1)
    model.fit(pd.DataFrame(np.zeros((2, 10)), columns=serve.FEATURE_NAMES), [0, 1])
    path = tmp_path / 'model.joblib'
    joblib.dump(model, path)
    monkeypatch.setattr(serve, 'download_model', lambda: path)
    with TestClient(serve.app) as api:
        yield api


def test_healthz(client):
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_score(client):
    response = client.post('/score', json={'features': [28, 2, 14, 2, 11, 0, 1, 0, 0, 45]})
    assert response.status_code == 200
    assert response.json() == {'prediction': 1, 'label': 'thu_nhap_cao'}


def test_wrong_feature_count(client):
    assert client.post('/score', json={'features': [1, 2]}).status_code == 400


def test_invalid_feature_type(client):
    assert client.post('/score', json={'features': ['invalid'] * 10}).status_code == 422


def test_download_model(tmp_path, monkeypatch):
    path = tmp_path / 'models' / 'model.joblib'
    monkeypatch.setenv('MODEL_PATH', str(path))
    monkeypatch.setenv('ARTIFACT_BUCKET', 'test-container')
    monkeypatch.setenv('AZURE_STORAGE_CONNECTION_STRING', 'test-connection')
    factory = MagicMock()
    client = factory.from_connection_string.return_value.__enter__.return_value
    blob = client.get_blob_client.return_value
    blob.download_blob.return_value.readinto.side_effect = lambda stream: stream.write(b'model bytes')
    monkeypatch.setattr(serve, 'BlobServiceClient', factory)
    assert serve.download_model() == path
    assert path.read_bytes() == b'model bytes'
    client.get_blob_client.assert_called_once_with('test-container', serve.MODEL_KEY)
    assert not path.with_suffix('.download').exists()
