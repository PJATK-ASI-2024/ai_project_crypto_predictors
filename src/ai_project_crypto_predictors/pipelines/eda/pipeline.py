from kedro.pipeline import Pipeline, node
from .nodes import load_data, describe_data, visualize_data

def create_pipeline(**kwargs):
    return Pipeline([
        node(load_data, "raw_data", "eda_data"),
        node(describe_data, "eda_data", "eda_summary"),
        node(visualize_data, "eda_data", None)
    ])
