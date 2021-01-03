#!python
import sys, logging
from logging import info, INFO, basicConfig, FileHandler

sys.path.append(".\\scripts")

from config.app_config import read_ci_function
from config.op import MESSAGE
from process.process import PasData, match
from process.output import write_output
from data.sort_data import sort_pas_data

CI_FUNCTION_PATH = ".\\config\\ci_function.txt"
LH_PATH = ".\\spread_sheets\\LH"
SH_PATH = ".\\spread_sheets\\SH"
LH_MIN_RC = (17, 2) # min_row, min_col
SH_MIN_RC = (2, 1)

def configure_logging():
    format = "%(process)d - %(asctime)s: %(message)s"
    LOG_FILE = ".\\logs\\app.log"

    basicConfig(
        format=format,
        datefmt="%H:%M:%S",
        level=INFO,
        handlers=[FileHandler(LOG_FILE, 'w', 'utf-8')],
    )

def log_dict(d, dict_name):
    info(f"*** {dict_name} ***\n")
    for k, v in d.items():
        info(f"[+] Key: {k}")
        info(f"[+] Values: {v}")
        info("\n")
    info(f"*** End {dict_name} ***\n")

def log_nested(d, dict_name):
    info(f"*** {dict_name} ***")
    for k, v in d.items():
        info(f"[+] Key: {k}")
        for i in v:
            info(f"[+] Nested list: {i}")
        info("\n\n")
    info(f"*** End {dict_name} ***\n")
    
def log_count(d, dict_name):
    info(f"Item count: {len(d)}")
    for k, v in d.items():
        info(f"Parent List Length: {len(v)}")
        for i in v:
            info(f"List Length: {len(i)}")
        info("\n")
    info("CI Functions Processed:")
    for k in d.keys():
        info(k)


if __name__ == '__main__':

    # ===| configure logging | ===
    print(MESSAGE['log'])
    configure_logging()
    # =====================================

    # ===| read ci function data |===
    print(MESSAGE['config'])
    ci_function_data = read_ci_function(CI_FUNCTION_PATH)
    log_dict(ci_function_data, "ci function data")
    # =====================================

    # ===| read spread sheet data | ===
    print(MESSAGE['read'])
    pas_object = PasData(LH_PATH, LH_MIN_RC)
    pas_object.read_sheets()
    #log_dict(pas_object.data, "data")
    # =====================================

    # ===| map the data to ci function |===
    print(MESSAGE['map'])
    mapped_data = match(ci_function_data, pas_object.data)
    # log_dict(mapped_data, "mapped data")
    # log_count(mapped_data, "counts")
    # =====================================

    # ===| extract relevant data and return new dictionary |===
    print(MESSAGE['sort'])
    rel_data = sort_pas_data(mapped_data)
    log_nested(rel_data, "relevant data")
    log_count(rel_data, "data count")
    # =====================================

    # === | format and write output strings | ===
    print(MESSAGE['write'])
    write_output(rel_data)

    # =====================================

    print(MESSAGE['done'])

    # TODO: Duplicates and child, operational output strings




