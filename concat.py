#!/usr/bin/env python
import os
from sys import argv, exit

def get_files(directory):
    return [os.path.join(directory, x) for x in os.listdir(directory)]
    
def read_files(files):
    archive = ""
    for f in files:
        try:
            with open(f, 'r+') as read_file:
                content = "".join(read_file.readlines())
        except BaseException as b_ex:
            print(f"[x] {b_ex}")
        else:
            archive += content
        finally:
            read_file.close()
    return archive

def write_file(archive, output_directory):

    file_name = os.path.join(output_directory, "cc_out.csv")
    
    try:
        with open(file_name, "w+") as output_file:
            for line in archive:
                output_file.write(line + "\n")
    except BaseException as base_ex:
        print(f"[x] {base_ex}")
    finally:
        output_file.close()

    print("[+] Concatenation complete!")

def concatenate(output_directory):

    files = get_files(output_directory)
    archive = read_files(files)
    write_file(archive, output_directory)