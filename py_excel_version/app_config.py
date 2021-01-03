#!python
import os

def read_ci_function(file_path):
    # Read the ci function data from .\\config\\ci_function.txt
    # Returns the data as a dict()
    try:
        with open(file_path, 'r+') as f:
            data = {x.strip("\n").split(":")[0]: [c.lstrip(" ") for c in x.strip("\n").split(":")[1].split(",")] for x in f.readlines()}
    except Exception as e:
        print(f"[x] Error: {e}")
    finally: f.close()
    return data
