import os
import sys

report_dir: str = "reports"
log_dir: str = "logs"
out_file: str = "out.docx"

# determine if application is a script file or frozen exe
data_dir: list[str] = []
if getattr(sys, "frozen", False):
    data_dir = ["data"]
    application_path = os.path.dirname(sys.executable)
else:
    data_dir = ["..", "data"]
    application_path = os.path.dirname(__file__)

main_path = os.path.join(application_path, *data_dir)

if not os.path.exists(main_path):
    os.makedirs(main_path)

report_path = os.path.join(main_path, report_dir)

if not os.path.exists(report_path):
    os.makedirs(report_path)

out_path = os.path.join(report_path, out_file)

logs_path = os.path.join(main_path, log_dir)
log_path = os.path.join(logs_path, "ffw-geraetewart.logs")

if not os.path.exists(logs_path):
    os.makedirs(logs_path)
