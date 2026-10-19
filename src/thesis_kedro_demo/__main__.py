from kedro.framework.cli.utils import find_run_command
from kedro.framework.project import configure_project


def main() -> None:
    configure_project("thesis_kedro_demo")
    find_run_command("thesis_kedro_demo")()


if __name__ == "__main__":
    main()
