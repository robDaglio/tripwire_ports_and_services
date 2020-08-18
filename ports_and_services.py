#!/usr/bin/env python
import sys
sys.path.append(".\\config")
sys.path.append(".\\scripts")
from app_config import (
    read_ci_function,
    get_input_file_path,
)
from process import (
    process_files,
    create_output_directory,
)
from duplicates import (
    process_duplicates,
    write_output_archive,
)

PAS_PATH = ".\\scripts\\pas.ps1"
PASLH_PATH = ".\\scripts\\paslh.ps1"
INPUT_FILES_LH = ".\\spread_sheets\\LH"
INPUT_FILES_SH = ".\\spread_sheets\\SH"
CI_FUNCTION = ".\\config\\ci_function.txt"

def run():

    # Returns dict() -> file_name: file_path
    input_long_header = get_input_file_path(INPUT_FILES_LH)
    input_short_header = get_input_file_path(INPUT_FILES_SH)

    # Returns dict() -> spread_sheet: ci_function
    ci_function_list = read_ci_function(CI_FUNCTION)

    # Creates output directory for current run at ".\\processed\date_time"
    output_directory = create_output_directory()

    for spread_sheet, ci_function in ci_function_list.items():       
        if spread_sheet in input_short_header.keys():
            process_files(ci_function, input_short_header[spread_sheet], PAS_PATH, output_directory)
        
        if spread_sheet in input_long_header.keys():
            process_files(ci_function, input_long_header[spread_sheet], PASLH_PATH, output_directory)

    # Concatenate results, remove duplicate entries and write cc_out
    archive = process_duplicates(output_directory, ci_function_list)
    write_output_archive(archive, output_directory)

if __name__ == '__main__':
    run()