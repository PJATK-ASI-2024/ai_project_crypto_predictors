"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from ai_project_crypto_predictors.pipelines import eda as eda_pipeline
from ai_project_crypto_predictors.pipelines import preprocessing as preprocessing_pipeline
from ai_project_crypto_predictors.pipelines import modeling as modeling_pipeline

def register_pipelines():
    return {
        "__default__": eda_pipeline.create_pipeline(),
        "eda": eda_pipeline.create_pipeline(),
        "preprocessing": preprocessing_pipeline.create_pipeline(),
        "modeling": modeling_pipeline.create_pipeline(),
    }
