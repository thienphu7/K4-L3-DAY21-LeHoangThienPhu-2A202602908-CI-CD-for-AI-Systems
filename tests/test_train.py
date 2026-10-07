import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import accuracy_score, f1_score
from src.train import train

FEATURE_NAMES = ['age', 'workclass', 'education_num', 'marital_status', 'occupation',
                 'relationship', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week']


def _make_temp_data(tmp_path):
    rng = np.random.default_rng(0)
    df = pd.DataFrame(rng.random((200, 10)), columns=FEATURE_NAMES)
    df['target'] = rng.integers(0, 2, size=200)
    train_path, eval_path = tmp_path / 'train.csv', tmp_path / 'holdout.csv'
    df.iloc[:160].to_csv(train_path, index=False)
    df.iloc[160:].to_csv(eval_path, index=False)
    return str(train_path), str(eval_path)


@pytest.fixture
def trained(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv('MLFLOW_TRACKING_URI', 'sqlite:///mlflow.db')
    monkeypatch.setenv('MLFLOW_ARTIFACT_ROOT', str(tmp_path / 'mlartifacts'))
    train_path, eval_path = _make_temp_data(tmp_path)
    f1 = train({'n_estimators': 10, 'learning_rate': 0.1, 'max_depth': 2},
               data_path=train_path, eval_path=eval_path)
    return f1, eval_path


def test_train_returns_float(trained):
    assert isinstance(trained[0], float)
    assert 0 <= trained[0] <= 1


def test_report_file_created(trained):
    report = json.loads(Path('outputs/report.json').read_text())
    assert report['f1_score'] == trained[0]
    assert 0 <= report['accuracy'] <= 1


def test_model_file_created(trained):
    model = joblib.load('models/model.joblib')
    df = pd.read_csv(trained[1])
    predictions = model.predict(df[FEATURE_NAMES])
    report = json.loads(Path('outputs/report.json').read_text())
    assert f1_score(df['target'], predictions) == report['f1_score']
    assert accuracy_score(df['target'], predictions) == report['accuracy']
