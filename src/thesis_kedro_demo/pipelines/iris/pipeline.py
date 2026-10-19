from kedro.pipeline import Pipeline, node, pipeline

from .nodes import split_data, train_and_evaluate, transform_data, validate_data


def create_pipeline() -> Pipeline:
    return pipeline([
        node(
            validate_data,
            ["iris_raw", "params:features", "params:target", "params:allowed_classes", "params:expected_rows"],
            "iris_validated",
            name="validate_data",
        ),
        node(
            transform_data,
            ["iris_validated", "params:features", "params:target"],
            "iris_clean",
            name="transform_data",
        ),
        node(
            split_data,
            ["iris_clean", "params:features", "params:target", "params:test_size", "params:random_state"],
            ["X_train", "X_test", "y_train", "y_test"],
            name="split_data",
        ),
        node(
            train_and_evaluate,
            ["X_train", "X_test", "y_train", "y_test", "params:model_options", "params:random_state", "params:allowed_classes"],
            ["iris_model", "iris_metrics"],
            name="train_and_evaluate",
        ),
    ])
