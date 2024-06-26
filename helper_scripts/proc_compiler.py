from helper_scripts.logger import Logger
import helper_scripts.default_values as dv

import subprocess
import os

class ProcResult:
    """
    Class representing a processor and its results. 
    """
    def __init__(self, name, expected):
        self.name = name
        self.expected = expected
        self.actual = []
        self.failed = []
    
    # TODO: maybe shouldn't be a static function?
    def read_exp(folder):
        """
        Reads the expected results from the given folder.
        """

        file_path = os.path.join(folder, 'exp.txt')
        lines = []

        # Open the file and read lines
        try:
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            Logger.warn(f"exp.txt not found for processor in folder {folder}. Defaulting to empty list.")
            return []
        
        # Return the list of lines
        return lines

def file_list(proc_folder):
    """
    Generates FileList.txt using the dedicated Wrapper_tb.v file
    """
    
    # Run the find command to get a list of .v files and store the result in FileList.txt
    os.system('find . -name "*.v" | grep -v "Wrapper_tb.v" > FileList.txt')
    
    # Read the contents of FileList.txt and remove lines containing "Wrapper_tb.v"
    with open('FileList.txt', 'r') as file:
        lines = file.readlines()
    
    # Write back the modified lines and add the additional line
    with open('FileList.txt', 'w') as file:
        file.writelines(lines)
        file.write(f'{dv.WRAPPER_PATH}\n')

def compile_proc(proc_folder, test_name):
    """
    Compiles the processor in the given folder with the given test name.
    Returns True if the test passes, False otherwise.
    """

    # Generate FileList
    file_list(proc_folder)
    
    Logger.info(f"Compiling processor {proc_folder} with test: {test_name}.")
    # Compile using iverilog
    compile_cmd = f'iverilog -o proc -c FileList.txt -s Wrapper_tb -P Wrapper_tb.FILE=\\\"{test_name}\\\"'
    compile_process = subprocess.Popen(compile_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    compile_output, compile_error = compile_process.communicate()
    Logger.iverilog(f"Compiler output: \n {compile_output.decode('utf-8')}")
    if compile_error:
        Logger.warn(f"iverilog compilation error: \n{compile_error.decode('utf-8')}")  
    
    # Run vvp
    run_cmd = 'vvp proc'
    run_process = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    run_output, run_error = run_process.communicate()
    run_output = run_output.decode('utf-8')

    Logger.iverilog(f"Simulation output: \n {run_output}")
    if run_error:
        Logger.warn(f"iverilog runtime error: \n {run_error}")

    # Find result 
    # TODO: maybe better way of doing this? 
    index_finished = run_output.rfind("Finished:")
    if index_finished == -1:
        Logger.warn("Simultion failed to run")
        return -1
    
    result = run_output[index_finished + len("Finished:")]

    return 1 if (result == 'P') else 0

def compile_all_procs(tests, procs_folder="example"):
    """
    Compiles all processors in the given folder.
    """

    # Check if procs_folder and tests_folder exist
    if not os.path.exists(procs_folder):
        Logger.error(f"Processor directory '{procs_folder}' does not exist.")
        sys.exit(1)

    proc_results = []
    original_directory = os.getcwd()

    for proc in os.listdir(procs_folder):
        if os.path.isdir(os.path.join(procs_folder, proc)):
            proc_folder = os.path.join(procs_folder, proc)
            current_proc = ProcResult(proc, ProcResult.read_exp(proc_folder))

            # Change directory to proc_folder
            os.chdir(proc_folder)

            for test in tests:
                res = compile_proc(proc_folder, test)
                if(res == 1):
                    current_proc.actual.append(test)
                elif(res == -1):
                    current_proc.failed.append(test)
            proc_results.append(current_proc)

            # Change directory back to original
            os.chdir(original_directory)
            Logger.info(f"Processor {proc} compiled successfully.")

    sorted_results = sorted(proc_results, key=lambda x: x.name)
    return sorted_results

if __name__ == "__main__":
    Logger.setup(log_level="INFO", output_destination="TERM")
    procs_folder = 'procs'  
    tests = ["alu_bypass", "alu_double_bypass", "bad"]
    results = compile_all_procs(procs_folder, tests)

    for result in results:
        print(f"Processor: {result.name}")
        print(f"Expected: {result.expected}")
        print(f"Actual: {result.actual}")
        print("--------------------")


