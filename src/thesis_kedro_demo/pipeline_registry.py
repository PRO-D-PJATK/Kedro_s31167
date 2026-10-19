from kedro.pipeline import Pipeline

from thesis_kedro_demo.pipelines.iris import create_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    pipeline = create_pipeline()
    return {"__default__": pipeline, "iris": pipeline}
