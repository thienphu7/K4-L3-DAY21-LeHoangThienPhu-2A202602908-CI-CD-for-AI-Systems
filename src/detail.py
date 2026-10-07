"""Create the per-class evaluation artifact from the model selected for serving."""
import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix


def create_detail(model_path='models/model.joblib', data_path='data/holdout.csv',
                  report_path='outputs/report.json', output_path='outputs/detail.txt'):
    model = joblib.load(model_path)
    df = pd.read_csv(data_path)
    threshold = json.loads(Path(report_path).read_text())['best_threshold']
    predictions = (model.predict_proba(df.drop(columns=['target']))[:, 1] >= threshold).astype(int)
    text = (f'Decision threshold: {threshold}\n'
            'Threshold was selected on this holdout; metrics are not an independent test estimate.\n'
            'Confusion matrix: rows=true, columns=predicted; class order=[0, 1]\n'
            f'{confusion_matrix(df.target, predictions, labels=[0, 1])}\n\n' +
            classification_report(df.target, predictions, labels=[0, 1],
                                  target_names=['thu_nhap_thap', 'thu_nhap_cao'],
                                  digits=6, zero_division=0))
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(text, encoding='utf-8')
    print(text)
    return text


if __name__ == '__main__':
    create_detail()
