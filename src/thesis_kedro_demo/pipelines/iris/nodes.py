from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split


def validate_data(
    data: pd.DataFrame,
    features: list[str],
    target: str,
    allowed_classes: list[str],
    expected_rows: int,
) -> pd.DataFrame:
    required = features + [target]
    if list(data.columns) != required:
        raise ValueError(f"Expected ordered columns: {required}")
    if len(data) != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows, received {len(data)}")
    if data.isna().any().any():
        raise ValueError("Missing values are not allowed")
    numeric = data[features].apply(pd.to_numeric, errors="raise")
    if not np.isfinite(numeric.to_numpy()).all() or (numeric <= 0).any().any():
        raise ValueError("Measurements must be finite and positive")
    labels = data[target].astype(str).str.strip()
    if set(labels) != set(allowed_classes):
        raise ValueError("Unexpected or missing species")
    return data.copy()


def transform_data(data: pd.DataFrame, features: list[str], target: str) -> pd.DataFrame:
    result = data.copy()
    result[features] = result[features].apply(pd.to_numeric, errors="raise").astype(float)
    result[target] = result[target].astype(str).str.strip()
    return result[features + [target]].reset_index(drop=True)


def split_data(
    data: pd.DataFrame,
    features: list[str],
    target: str,
    test_size: float,
    random_state: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between zero and one")
    return tuple(train_test_split(
        data[features],
        data[target],
        test_size=test_size,
        random_state=random_state,
        stratify=data[target],
    ))


def train_and_evaluate(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    model_options: dict[str, Any],
    random_state: int,
    allowed_classes: list[str],
) -> tuple[RandomForestClassifier, dict[str, Any]]:
    model = RandomForestClassifier(random_state=random_state, **model_options)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "f1_macro": float(f1_score(y_test, predictions, average="macro")),
        "classification_report": classification_report(
            y_test, predictions, labels=allowed_classes, output_dict=True, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=allowed_classes).tolist(),
        "class_order": allowed_classes,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "random_state": random_state,
        "model_parameters": model.get_params(),
    }
    return model, metrics
