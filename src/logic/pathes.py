import os
import sys

data_dir = "data"
report_dir = "reports"
out_file = "out.docx"

# determine if application is a script file or frozen exe
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(__file__)

main_path = os.path.join(application_path, data_dir)

if not os.path.exists(main_path):
    print(f"create main_path because it doesnt exist ({main_path})")
    os.makedirs(main_path)

report_path = os.path.join(main_path, report_dir)

if not os.path.exists(report_path):
    print(f"create main_path because it doesnt exist ({report_path})")
    os.makedirs(report_path)

out_path = os.path.join(report_path, out_file)
