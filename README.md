# Thesis Kedro Demo

A minimal Kedro project that predicts Iris species from four flower measurements using a Random Forest classifier. Four typed, pure-ish nodes validate the CSV, transform its columns, create a stratified holdout, and train/evaluate the model. Kedro handles all data loading and saving through named catalog datasets. Node code contains no comments, filesystem paths, or direct file access.

## Dataset and attribution

The project bundles 150 rows from the UCI Iris dataset, with four measurements in centimetres and three species. No download is needed to run it.

- Public dataset: https://archive.ics.uci.edu/dataset/53/iris
- Public archive: https://archive.ics.uci.edu/static/public/53/iris.zip
- Citation: Fisher, R. A. (1936). Iris [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C56C76
- License: CC BY 4.0, as listed by UCI: https://creativecommons.org/licenses/by/4.0/

The CSV adds a header to the archive's `iris.data` and removes empty lines, preserving every measurement and species label. See `DATA_LICENSE.md` for attribution and changes. The original dataset can contain repeated measurements; these are retained. This is a small educational holdout evaluation, not a claim of performance on new real-world populations.

## Install and run

Use Python 3.12 for the tested setup. The project declares Python 3.10–3.12; Python 3.9 from the assignment's general prerequisites is insufficient for these pinned dependencies.

From the extracted project directory, on macOS/Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
kedro run
```

On Windows PowerShell, create the environment with `py -3.12 -m venv .venv` and activate it with `.venv\Scripts\Activate.ps1`, then use the same install/run commands.

The named pipeline is also available:

```bash
kedro run --pipeline=iris
```

Kedro finds `src/` using `pyproject.toml`; installing the project package itself is optional. This is a hand-scaffolded minimal project with the standard Kedro layout, requiring no starter download.

## Layout

```text
thesis_kedro_demo/
├── conf/
│   ├── base/
│   │   ├── catalog.yml
│   │   └── parameters.yml
│   ├── local/.gitkeep
│   └── smoke/parameters.yml
├── data/
│   ├── 01_raw/iris.csv
│   ├── 01_raw/SHA256SUMS
│   ├── 02_intermediate/iris_clean.csv
│   ├── 06_models/iris_model.pkl
│   └── 08_reporting/metrics.json
├── src/thesis_kedro_demo/
│   ├── __init__.py
│   ├── __main__.py
│   ├── settings.py
│   ├── pipeline_registry.py
│   └── pipelines/iris/
│       ├── __init__.py
│       ├── nodes.py
│       └── pipeline.py
├── .gitignore
├── .telemetry
├── DATA_LICENSE.md
├── README.md
├── VALIDATION.md
├── pyproject.toml
├── requirements.txt
└── requirements-lock.txt
```

Generated CSV/model/metrics are included as evidence in the zip and overwritten on a full run. Git ignores generated data; the raw CSV, catalog, parameters, source, and documentation should be committed. Intermediate split datasets remain in memory. Empty directories contain `.gitkeep` files.

## Pipeline and catalog

| Node | Inputs | Outputs |
| --- | --- | --- |
| `validate_data` | `iris_raw`, schema/class parameters | `iris_validated` |
| `transform_data` | validated data, feature/target names | `iris_clean` |
| `split_data` | cleaned data, feature/target names, split/seed | `X_train`, `X_test`, `y_train`, `y_test` |
| `train_and_evaluate` | split data, model options, seed, class order | `iris_model`, `iris_metrics` |

Validation rejects incorrect columns, row count, missing values, nonnumeric/nonpositive/nonfinite measurements, and unexpected or absent species. Transformation converts measurements to floats and strips whitespace from labels. Splitting is stratified and seeded. Training uses only the training subset; evaluation uses the holdout. A Random Forest does not require feature scaling.

`conf/base/catalog.yml` declares the raw and cleaned data as `pandas.CSVDataset`, the model as `pickle.PickleDataset`, and the report as `json.JSONDataset`. Temporary datasets explicitly use `MemoryDataset`. All persisted paths are relative to the project root and defined only in configuration.

The report includes accuracy, macro F1, per-class precision/recall/F1, a confusion matrix with class order, split sizes, seed, and model parameters. The model artifact is a fitted `RandomForestClassifier`; only load pickle files you trust.

## Parameters and environments

`conf/base/parameters.yml` holds feature names, target, allowed species, expected rows, test size (`0.2`), random seed (`42`), and Random Forest options (`100` trees, maximum depth `4`, one worker).

```bash
kedro run --params=test_size=0.3,random_state=7
kedro run --env=smoke
```

`base` provides shared defaults. The default runtime environment is `local`; add machine-specific overrides and credentials under `conf/local/`, whose contents are ignored except `.gitkeep`. Never commit secrets. `smoke` overlays the base parameters and reduces the forest to 10 trees for a quick demonstration; it uses the same data and output paths, overwriting the default artifacts. Run `kedro run` afterward to restore the default results. Changing `expected_rows` is necessary when intentionally using another dataset size.

## Reproducibility

Validated with Python 3.12.14 and Kedro 0.19.14. Direct dependencies are pinned in `requirements.txt`; the complete resolved environment is recorded in `requirements-lock.txt`. For the closest recreation on Python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip check
kedro run
```

The full lock is a pip freeze snapshot without artifact hashes, rather than a cross-platform resolver lock. Other platforms/Python versions have not been verified. Fixed data order, the bundled CSV checksum, deterministic stratified splitting, fixed model seed, and one worker make repeated runs in the validated environment produce matching metrics. No timestamps enter the metrics. Bitwise identical model files across platforms or library versions are not guaranteed.

The CSV SHA-256 is stored beside it. From `data/01_raw`, run `shasum -a 256 -c SHA256SUMS` on macOS or `sha256sum -c SHA256SUMS` on Linux. See `VALIDATION.md` for actual run results and checks. Run the pipeline from the project root. Network access is needed for dependency installation, not pipeline execution. Telemetry consent is disabled in `.telemetry`.

## Publishing the assignment

No GitHub repository has been created by this deliverable. To publish, create an empty repository on GitHub, then run the following in this project directory, replacing the final URL with your actual repository URL:

```bash
git init
git add .
git commit -m "Add reproducible Kedro Iris project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/thesis_kedro_demo.git
git push -u origin main
```

Review staged files before committing and keep credentials under `conf/local/`. Repository creation and a push are still required for the assignment's GitHub deliverable.
