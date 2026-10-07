import json
import os

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score

F1_THRESHOLD = 0.65


def train(params: dict, data_path: str = "data/train_batch1.csv",
          eval_path: str = "data/holdout.csv") -> float:
    """Train and return positive-class holdout F1; save deployment artifacts."""
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))
    experiment_name = "adult-income"
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        from pathlib import Path
        artifact_root = Path(os.environ.get("MLFLOW_ARTIFACT_ROOT", "./mlartifacts"))
        mlflow.create_experiment(experiment_name, artifact_location=artifact_root.resolve().as_uri())
    mlflow.set_experiment(experiment_name)
    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)
    X_train, y_train = df_train.drop(columns=["target"]), df_train["target"]
    X_eval, y_eval = df_eval.drop(columns=["target"]), df_eval["target"]
    with mlflow.start_run():
        mlflow.log_params(params)
        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)
        preds = model.predict(X_eval)
        f1 = float(f1_score(y_eval, preds))
        acc = float(accuracy_score(y_eval, preds))
        mlflow.log_metrics({"f1_score": f1, "accuracy": acc})
        mlflow.sklearn.log_model(model, "model")
        print(f"F1: {f1:.4f} | Accuracy: {acc:.4f}")
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/report.json", "w", encoding="utf-8") as f:
            json.dump({"f1_score": f1, "accuracy": acc}, f, indent=2)
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.joblib")
    return f1


if __name__ == "__main__":
    with open("params.yaml", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    train(params)
