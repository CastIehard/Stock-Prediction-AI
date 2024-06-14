import subprocess
import os
from my_config import output_bool

# Get the current working directory
cwd = os.path.dirname(os.path.abspath(__file__))
python3_path = os.path.join(cwd, ".venv/bin/python3")

#run data collector
path = os.path.join(cwd, "2_data_collector.py")
subprocess.run([python3_path,path])
if output_bool:
    print("Data Collector finished")

#put data into one big csv
path = os.path.join(cwd, "3_json_2_csv.py")
subprocess.run([python3_path,path])
if output_bool:
    print("Json to CSV finished")

#run mail writer
path = os.path.join(cwd, "4_mail_sender.py")
subprocess.run([python3_path,path])
if output_bool:
    print("Mail Sender finished")
