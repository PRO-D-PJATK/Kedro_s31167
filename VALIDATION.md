# Validation results

Validated on 2026-10-19 with Python 3.12.14 on macOS ARM64, Kedro 0.19.14, kedro-datasets 6.0.0, pandas 2.2.3, NumPy 2.2.6, and scikit-learn 1.6.1.

- Fresh virtual environment: requirements installed successfully.
- `python -m pip check`: no broken requirements found.
- `kedro run`: completed all four nodes and persisted cleaned CSV, fitted model, and JSON metrics.
- `kedro run --env=smoke`: completed all four nodes with 10 trees.
- `kedro run --pipeline=iris`: completed all four nodes and restored default artifacts.
- Default metrics matched byte-for-byte across the first and repeat runs.
- Training rows: 120; holdout rows: 30; 10 holdout rows per species.
- Holdout accuracy: 0.9666666667 (29 of 30 correct).
- Macro F1: 0.9665831245.
- Seven invalid-data cases rejected: missing column, wrong row count, null, infinity, negative measurement, unexpected species, and nonnumeric measurement.
- Validation/transformation left input data unchanged; split indices were disjoint.
- Every Python source parsed successfully and contained zero comment tokens.
- Source data checksum matched `data/01_raw/SHA256SUMS`.

The installed Kedro/dependency combination emits upstream deprecation warnings; these did not prevent successful execution. The resolved dependency versions are recorded in `requirements-lock.txt`. No GitHub repository was created or pushed.

Generated artifacts in this archive are from the final default-parameter run. Only this Python/platform combination was executed.
