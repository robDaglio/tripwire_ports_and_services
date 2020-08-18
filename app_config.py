#!/usr/bin/env python
import os

def read_ci_function(ci_function_path):
    try:
        with open(ci_function_path, 'r+') as input_file:
            content = {x.split('"')[1]: x.split('"')[3] for x in input_file.readlines()}
    except BaseException as e:
        print(f"[x] Error: {e}")
    else:
        return content
    finally:
        input_file.close()

def get_input_file_path(input_files):
    abs_path = os.path.abspath(input_files)
    files = {x: os.path.join(abs_path, x) for x in os.listdir(input_files)}
    
    return files