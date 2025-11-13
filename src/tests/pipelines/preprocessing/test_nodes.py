import pandas as pd
import numpy as np
from ai_project_crypto_predictors.pipelines.preprocessing.nodes import clean_data, scale_data, split_data

def test_clean_data_removes_nulls():
    df = pd.DataFrame({"a": [1, 2, np.nan], "b": ["3", "4", "5"]})
    result = clean_data(df)
    assert not result.isnull().any().any()
    assert len(result) > 0

def test_scale_data_standardization():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5]})
    scaled = scale_data(df)
    np.testing.assert_almost_equal(scaled.mean().values, 0, decimal=1)
    np.testing.assert_almost_equal(scaled.std().values, 1, decimal=1)

def test_split_data_shapes():
    df = pd.DataFrame({"x": range(100)})
    train, val, test = split_data(df)
    total = len(train) + len(val) + len(test)
    assert total == len(df)
    assert 0.6 < len(train) / total < 0.8
