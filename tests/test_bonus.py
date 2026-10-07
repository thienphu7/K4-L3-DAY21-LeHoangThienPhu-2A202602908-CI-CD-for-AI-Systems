import json
from unittest.mock import MagicMock
import numpy as np
import pytest
from azure.core.exceptions import ResourceNotFoundError
from src.release import deployment_allowed, publish
from src.train import check_class_distribution, select_threshold


@pytest.mark.parametrize('candidate,current,allowed',[(0.74,0.73,True),(0.73,0.73,True),(0.70,0.73,False)])
def test_regression_gate(candidate,current,allowed):
    assert deployment_allowed({'f1_score':candidate},{'f1_score':current}) is allowed


@pytest.mark.parametrize('score',[0.64,float('nan'),float('inf'),1.1])
def test_invalid_candidate(score):
    with pytest.raises(ValueError): deployment_allowed({'f1_score':score},None)


def test_rejected_candidate_does_not_upload(tmp_path):
    client=MagicMock()
    client.get_blob_client.return_value.download_blob.return_value.readall.return_value=b'{"f1_score":0.8}'
    assert not publish(client,'container',tmp_path/'missing-model',{'f1_score':0.7},'test')
    client.get_blob_client.return_value.upload_blob.assert_not_called()


def test_first_deploy_publishes_version_and_report(tmp_path):
    client=MagicMock()
    client.get_blob_client.return_value.download_blob.side_effect=ResourceNotFoundError('missing')
    path=tmp_path/'model';path.write_bytes(b'model')
    assert publish(client,'container',path,{'f1_score':0.8},'test')
    assert client.get_blob_client.return_value.upload_blob.call_count==4


def test_drift_warning(capsys):
    import pandas as pd
    ratio,warning=check_class_distribution(pd.Series([0,1]*5))
    assert warning and ratio==0.5
    assert 'WARNING: DATA DRIFT' in capsys.readouterr().out


def test_reference_distribution(capsys):
    import pandas as pd
    _,warning=check_class_distribution(pd.Series([1]*248+[0]*752))
    assert not warning
    assert 'DATA DISTRIBUTION OK' in capsys.readouterr().out


def test_threshold_sweep():
    y=np.array([0,0,1,1]);p=np.array([.1,.2,.35,.4])
    (threshold,f1),scores=select_threshold(y,p)
    assert f1==1 and .2 < threshold <= .35
    assert len(scores)==17 and scores[0]['threshold']==.1 and scores[-1]['threshold']==.9
