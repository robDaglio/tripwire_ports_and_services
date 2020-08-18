#!/usr/bin/env python
import os, sys, itertools
from app_config import (
    read_ci_function,
    get_input_file_path,
)

def modify_ci(ci_function):
    modified = dict()
    for k, v in ci_function.items():
        k = k.replace(".xlsx", ".csv")
        modified[k] = v
    return modified    

def read_data(file_name):
    try:
        with open(file_name, "r+") as input_file:
            data = [x.strip("\n") for x in input_file.readlines()]
    except BaseException as e:
        print("[x] Error")
    else:
        return data
    finally:
        input_file.close()

def write_output_archive(archive, output_directory):
    file_name = os.path.join(output_directory, "cc_out.csv")
    
    try:
        with open(file_name, "w+") as output_file:
            for line in archive:
                output_file.write(line + "\n")
    except BaseException as base_ex:
        print(f"[x] {base_ex}")
    finally:
        output_file.close()

    print("[+] Duplicates removed!")

def process_duplicates(file_path, ci):
    files = get_input_file_path(file_path)
    modified_ci_csv = modify_ci(ci)

    ci_data, archive = dict(), list()

    for file_name, ci_function in modified_ci_csv.items():
        if file_name in files.keys():
            if ci_function in ci_data.keys():
                data = read_data(files[file_name])
                ci_data[ci_function].append(data)
            else:    
                data = read_data(files[file_name])
                ci_data[ci_function] = list()
                ci_data[ci_function].append(data)
    
    for ci_function, data_list in ci_data.items():
        merged = list(itertools.chain.from_iterable(data_list))
        remove_duplicates = list(dict.fromkeys(merged))
        ci_data[ci_function] = remove_duplicates
    
    for ci_function, data in ci_data.items():
        for line in data:
            archive.append(line)
    
    return archive
            


    

            
    