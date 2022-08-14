import os
import sys


def __create_path(*args) -> str:
    return_path: str = os.path.join(*args)

    # ensure path exist
    if not os.path.exists(return_path):
        os.makedirs(return_path)

    return return_path


# determine if application is a script file or frozen exe
data_dir: list[str] = []
if getattr(sys, "frozen", False):
    data_dir = ["data"]
    application_path = os.path.dirname(sys.executable)
else:
    data_dir = ["..", "data"]
    application_path = os.path.dirname(__file__)


main_path: str = __create_path(application_path, *data_dir)
report_path: str = __create_path(main_path, "reports")
out_path: str = os.path.join(report_path, "out.docx")
logs_path: str = __create_path(main_path, "logs")
log_path: str = os.path.join(logs_path, "ffw-geraetewart.logs")
