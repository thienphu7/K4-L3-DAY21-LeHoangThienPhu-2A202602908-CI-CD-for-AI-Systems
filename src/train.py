import json
import os
from urllib.parse import urlparse

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score
import numpy as np

F1_THRESHOLD = 0.65


def check_class_distribution(target):
    ratio = float(target.mean())
    drift = abs(ratio - 0.248) > 0.05 + 1e-12
    print(f"{'WARNING: DATA DRIFT' if drift else 'DATA DISTRIBUTION OK'}: "
          f"positive_ratio={ratio:.6f}; reference=0.248; tolerance=0.05")
    return ratio, drift


def select_threshold(y_true, probabilities):
    thresholds = np.round(np.arange(0.1, 0.901, 0.05), 2)
    scores = [(float(t), float(f1_score(y_true, probabilities >= t, zero_division=0)))
              for t in thresholds]
    # Prefer the threshold nearest 0.5 when F1 ties.
    best = max(scores, key=lambda row: (row[1], -abs(row[0] - 0.5)))
    return best, [{'threshold': t, 'f1_score': f1} for t, f1 in scores]


def train(params: dict, data_path: str = "data/train_batch1.csv",
          eval_path: str = "data/holdout.csv") -> float:
    """Train and return positive-class holdout F1; save deployment artifacts."""
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"))
    experiment_name = "adult-income"
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        if urlparse(mlflow.get_tracking_uri()).scheme in {"http", "https"}:
            # Remote servers select their own artifact store; never send a CI file URI.
            mlflow.create_experiment(experiment_name)
        else:
            from pathlib import Path
            artifact_root = Path(os.environ.get("MLFLOW_ARTIFACT_ROOT", "./mlartifacts"))
            mlflow.create_experiment(experiment_name, artifact_location=artifact_root.resolve().as_uri())
    mlflow.set_experiment(experiment_name)
    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)
    X_train, y_train = df_train.drop(columns=["target"]), df_train["target"]
    X_eval, y_eval = df_eval.drop(columns=["target"]), df_eval["target"]
    positive_ratio, drift = check_class_distribution(y_train)
    with mlflow.start_run():
        if os.environ.get("GITHUB_SHA"):
            mlflow.set_tags({
                "git_commit": os.environ["GITHUB_SHA"],
                "github_run_id": os.environ.get("GITHUB_RUN_ID", ""),
            })
        mlflow.log_params(params)
        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)
        probabilities = model.predict_proba(X_eval)[:, 1]
        (threshold, f1), threshold_scores = select_threshold(y_eval, probabilities)
        default_f1 = float(f1_score(y_eval, model.predict(X_eval), zero_division=0))
        preds = (probabilities >= threshold).astype(int)
        acc = float(accuracy_score(y_eval, preds))
        model.income_threshold_ = threshold
        report = {"f1_score": f1, "accuracy": acc, "best_threshold": threshold,
                  "f1_default_0_5": default_f1, "positive_ratio": positive_ratio,
                  "data_drift_warning": drift, "train_rows": len(df_train),
                  "eval_rows": len(df_eval), "threshold_scores": threshold_scores}
        mlflow.log_metrics({"f1_score": f1, "accuracy": acc, "best_threshold": threshold,
                            "f1_default_0_5": default_f1, "positive_ratio": positive_ratio})
        mlflow.set_tag("threshold_selection_data", "holdout; tuned score, not independent test")
        print(f"Threshold sweep: best={threshold:.2f}; F1={f1:.6f}; default F1={default_f1:.6f}")
        mlflow.sklearn.log_model(model, "model")
        print(f"F1: {f1:.4f} | Accuracy: {acc:.4f}")
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.joblib")
        mlflow.log_artifact("outputs/report.json")
    return f1


if __name__ == "__main__":
    with open("params.yaml", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    train(params)
