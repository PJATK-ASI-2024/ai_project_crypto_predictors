from kedro.pipeline import Pipeline, node
from .nodes import clean_data, scale_data, split_data

def create_pipeline(**kwargs):
    return Pipeline([
        node(clean_data, "raw_data", "clean_data", name="clean_data_node"),
        node(scale_data, "clean_data", "scaled_data", name="scale_data_node"),
        node(split_data, "scaled_data", ["train_data", "val_data", "test_data"], name="split_data_node"),
    ])
