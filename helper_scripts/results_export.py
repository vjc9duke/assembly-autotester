from datetime import datetime
from logger import Logger
import os
import csv

import default_values as dv
from proc_compiler import compile_all_procs

def export_results(proc_results, tests, folder=dv.OUTPUT_DIR):
    """
    Given a list of ProcResults objects, consolidates all results and exports into a CSV file
    """
    # Prepare CSV file path
    curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = folder + "/" + curr_time
    csv_file_path = output_folder + "/results.csv"

    if not os.path.exists(folder):
        os.makedirs(folder)
        Logger.warn(f"Output folder '{folder}' does not exist. Creating it now.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Prepare CSV header
    fieldnames = ["processor name", "test name", "expected", "actual", "diff"]

    # Write data to CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through ProcResults
        for proc_result in proc_results:
            # Iterate through tests
            for test in tests:
                # Check if test is in expected or actual
                expected_val = 1 if test in proc_result.expected else 0
                actual_val = 1 if test in proc_result.actual else 0
                diff_val = actual_val - expected_val

                # Write row to CSV
                writer.writerow({
                    "processor name": proc_result.name,
                    "test name": test,
                    "expected": expected_val,
                    "actual": actual_val,
                    "diff": diff_val
                })

def get_tests(tests_folder):
    if not os.path.exists(tests_folder):
        Logger.error(f"Memory files directory '{tests_folder}' does not exist.")
        sys.exit(1)    

    tests = []
    for test_file in os.listdir(tests_folder):
        if os.path.isfile(os.path.join(tests_folder, test_file)):
            file_name, file_extension = os.path.splitext(test_file)
            if file_extension == ".mem":
                tests.append(file_name)
    return tests

if __name__ == "__main__":
    Logger.setup(log_level="INFO", output_destination="TERM")
    procs_folder = 'procs'  
    tests_folder = 'test_files/mem_files'
    tests = get_tests(tests_folder)

    proc_results = compile_all_procs(procs_folder, tests)
    export_results(proc_results, tests)