#!python
import os
from datetime import datetime

OUTPUT_PATH = ".\\processed"

def write_output(data):
    # Create output directory and return output path and proposed file name (WLP{time and date of run}.csv)
    output_path, file_name = create_output_directory()
    # Convert dictionary data to list of strings for writing
    output_list = convert_to_string(data)
    # Output file name formatting
    output_file_name = f"{output_path}\\WLP-{file_name}.csv"

    # Write output to file (WLP{time and date of run}.csv)
    try:
        with open(output_file_name, "w+") as output_file:
            for line in output_list:
                output_file.write(line + "\n")
    except Exception as e:
        print(f"[x] Error writing data: {e}")
        print(f"[!] Offending line: {line}")
    finally: output_file.close()
    # return output_list     # uncomment for logging purposes only 

def convert_to_string(data):    # Converts dictionary to list, using the key as the first field in the list
    output_list = list()

    # service       (data_set[0])
    # port          (data_set[1])
    # protocol      (data_set[2])
    # description   (data_set[3])
    # justification (data_set[4])
    # documentation (data_set[5])
    # page numbers  (data_set[6])

    for ci_function, d in data.items():
        output_list.append(f"## Authorized Ports for CIFunction - {ci_function}")
        for data_set in d:
            # Build string with data elements
            data_line = f'{ci_function}, {data_set[2]}, {data_set[1]}, {data_set[0]}, "{data_set[3]}", "{data_set[4]}", "{data_set[5]}", "{data_set[6]}"'
            # Remove all non-ASCII characters *** NECESSARY or throws encoding error when writing ***
            encoded = data_line.encode("ascii", "ignore")
            line = encoded.decode()
            # Append record to list
            output_list.append(line)
    return output_list

def create_output_directory():
    now = str(datetime.today()).split(".")[0].replace(":", "-").replace(" ", "_")
    output_path = os.path.join(OUTPUT_PATH, now)
    os.mkdir(output_path)

    return output_path, now  