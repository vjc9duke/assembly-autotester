import sys
import os
import yaml

from helper_scripts.logger import Logger
import helper_scripts.default_values as dv
import helper_scripts.asm_compiler as asm
import helper_scripts.proc_compiler as proc
import helper_scripts.results_export as rexp

def read_config(config_file):
    try:
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
            return config_data
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) > 2:
        print("Usage: python autotester.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1] if len(sys.argv) == 2 else dv.DEFAULT_CONFIG_FILE

    config_data = read_config(config_file)

    # Logging setup
    try:
        Logger.setup(log_level=config_data["LOG_LEVEL"], output_destination=config_data["LOG_LOC"], 
            rolling=config_data["LOG_ROLL"], folder_path=config_data["LOG_DIR"])
    except KeyError as e:
        print(f"Missing logging-related key in config file: {e}")
        sys.exit(1)

    Logger.info("Logger setup complete.")

    # Assemble all files
    try:
        asm.assemble_all(os_name=config_data["OS"])
    except KeyError as e:
        asm.assemble_all()
        Logger.warn(f"Missing OS key in config file. Defaulting to 'Linux'.")

    Logger.info("Assembly file compilation complete.")

    tests = get_tests("test_files/mem_files")
    # Compile all processors
    try:
        proc_results = proc.compile_all_procs(procs_folder=config_data["PROCS"], tests=tests)
    except KeyError as e:
        proc_results = proc.compile_all_procs()
        Logger.warn(f"Missing PROCS key in config file. Defaulting to 'example'.")

    Logger.info("Processor compilation complete.")

    # Export results
    try:
        rexp.export_results(proc_results, tests, rolling = config_data["OUT_ROLL"])
    except KeyError as e:
        rexp.export_results(proc_results, tests)
        Logger.warn(f"Missing OUT_ROLL key in config file. Defaulting to False.")
    
    Logger.info("Results exported.")
    Logger.close()

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
    main()
