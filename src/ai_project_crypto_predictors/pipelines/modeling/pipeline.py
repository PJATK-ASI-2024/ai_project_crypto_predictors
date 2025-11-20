from kedro.pipeline import Pipeline, node
from .nodes import (
    train_baseline,
    train_automl,
    train_custom,
    evaluate_models,
    persist_baseline,
    persist_automl,
    persist_custom,
)


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(train_baseline, ["train_data", "val_data"], ["baseline_model", "baseline_metrics"], name="train_baseline"),
            node(train_automl, ["train_data", "val_data"], ["automl_model", "automl_metrics"], name="train_automl"),
            node(train_custom, ["train_data", "val_data"], ["custom_model", "custom_metrics"], name="train_custom"),
            node(evaluate_models, ["baseline_metrics", "automl_metrics", "custom_metrics"], "model_comparison", name="evaluate_models"),

            node(persist_baseline, ["baseline_model", "baseline_metrics"], "baseline_persist_info", name="persist_baseline"),
            node(persist_automl, ["automl_model", "automl_metrics"], "automl_persist_info", name="persist_automl"),
            node(persist_custom, ["custom_model", "custom_metrics"], "custom_persist_info", name="persist_custom"),
        ]
    )
