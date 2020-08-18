import os, subprocess
from datetime import datetime

PS_PATH = "C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"
OUTPUT_PATH = ".\\processed"

def process_files(ci_function, spread_sheet, script, output_directory):
    command = subprocess.Popen(
        [
            PS_PATH, 
            "-ExecutionPolicy", 
            "Bypass", 
            "-NoLogo", 
            "-NoProfile", 
            "-File",
            script,
            ci_function,
            spread_sheet,
            output_directory, 
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    output = command.communicate()[0].decode("utf-8").strip("\n")
    print(output)

def create_output_directory():
    new = str(datetime.today()).split(".")[0].replace(":", "-").replace(" ", "_")
    output_path = os.path.join(OUTPUT_PATH, new)
    os.mkdir(output_path)

    return output_path
