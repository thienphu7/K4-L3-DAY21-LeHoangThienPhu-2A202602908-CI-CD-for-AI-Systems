"""Reject lower-F1 candidates before any production blob is modified."""
import hashlib
import json
import math
import os
from pathlib import Path
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient


def deployment_allowed(candidate, current):
    score = float(candidate['f1_score'])
    if not math.isfinite(score) or not 0.65 <= score <= 1:
        raise ValueError('Candidate does not pass F1 quality gate')
    if current is None:
        print(f'FIRST DEPLOY: candidate F1={score:.6f}; no production report')
        return True
    previous = float(current['f1_score'])
    if not math.isfinite(previous) or not 0 <= previous <= 1:
        raise ValueError('Invalid production F1; deployment stopped')
    allowed = score >= previous
    print(f"{'ALLOW' if allowed else 'BLOCK REGRESSION'}: candidate F1={score:.6f}; "
          f'production F1={previous:.6f}')
    return allowed


def publish(client, container, model_path, report, version):
    current_blob = client.get_blob_client(container, 'artifacts/current/report.json')
    try:
        current = json.loads(current_blob.download_blob().readall())
    except ResourceNotFoundError:
        current = None
    if not deployment_allowed(report, current):
        return False
    model = Path(model_path).read_bytes()
    if current and current.get('model_sha256'):
        live = client.get_blob_client(container, 'artifacts/current/model.joblib').download_blob().readall()
        if hashlib.sha256(live).hexdigest() != current['model_sha256']:
            raise ValueError('Production model/report mismatch; deployment stopped')
    report = dict(report, model_sha256=hashlib.sha256(model).hexdigest(), version=version)
    report_bytes = json.dumps(report, indent=2).encode()
    for prefix in [f'artifacts/versions/{version}', 'artifacts/current']:
        client.get_blob_client(container, prefix + '/model.joblib').upload_blob(model, overwrite=True)
        client.get_blob_client(container, prefix + '/report.json').upload_blob(report_bytes, overwrite=True)
    print(f'Published approved model and report: version={version}')
    return True


if __name__ == '__main__':
    with BlobServiceClient.from_connection_string(os.environ['AZURE_STORAGE_CONNECTION_STRING']) as client:
        allowed = publish(client, os.environ['ARTIFACT_BUCKET'], 'models/model.joblib',
                          json.loads(Path('outputs/report.json').read_text()),
                          os.environ['GITHUB_RUN_ID'] + '-' + os.environ.get('GITHUB_RUN_ATTEMPT', '1'))
    with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
        stream.write(f"deploy={'true' if allowed else 'false'}\n")
