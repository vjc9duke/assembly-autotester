# Assembly File Autotester
## Overview 
This repository provides an automated way to test new assembly files against known processors. All assembly files in the `test_files/assembly_files` directory will be automatically compiled and tested against the provided processors. The results are shown in console and printed to files in the `output` directory. 

## Configuration
The `config.yaml` configuration file provides numerous options for the autotester. The most important are:
* `PROCS`: The folder containing the processor files to test against. By default, this is routed to the `example` directory, which includes a single-cycle processor with only basic ALU support. 
* `OS`: The operating system of the host machine. This is used to determine the correct assembler to use for the assembly files. 


Parameters to configure the Logger are also available in the configuration file:
* `LOG_LEVEL`: The level of logging to use. By default, this is set to `INFO`.
    * `INFO`: logs completion of each step, and everything below.
    * `IVERILOG`: logs all iverilog output from processor compilation, and everything below.
    * `WARN`: logs recoverable errors (e.g., failed processor compilation), and everything below.
    * `ERROR`: logs unrecoverable errors (e.g., missing assembly files).
    * `NONE`: logs nothing.
* `LOG_LOC`: The location to output the log. This can be either `TERM` for console output or `FILE` for file output. 
* `LOG_DIR`: If `LOG_LOC` is set to `FILE`, this is where the log files are saved. 
* `LOG_ROLL`: Enables rolling log files. If set to `True`, only the five most recent files are kept in `LOG_DIR`.

Other parameters:
* `OUT_ROLL`: Enables rolling output files. If set to `True`, only the five most recent files are kept in the `output` directory.
* `FILT_ASM`: Enables filtering of the `test_files/assembly_files` directory. If set to `True`, only files listed in `test_files/assembly_files/active.txt` are tested.

## Usage
1. Run `pip install -r requirements.txt` to install the required packages.
2. Place the assembly files to test in the `test_files/assembly_files` directory and their expected files in the `test_files/verification_files` directory.
3. Place the processors in a folder of your choosing. 
    - **Each processor must also have an `exp.txt` file that lists all the tests it should pass**. You can see an example in `example/single-cycle-alu/exp.txt`. 
4. Configure the `config.yaml` file as needed. Remember to set `PROCS` and `OS` to the correct values. 
5. Run `python autotester.py` to run the autotester.
    - You may also specify a different configuration file by running `python autotester.py <config_file>`.

## Output
For each run, the autotester generates a new folder in the `output` directory with the current timestamp. This contains a summary `results.csv` file and a `diff.csv` file. Each file has the following columns:
* `processor name`: The name of the processor tested
* `test name`: The name of the test
* `expected`: The expected output of the test
* `actual`: The actual output of the test
    - 1 for pass
    - 0 for fail
    - -1 for failed to run
* `diff`: `actual` - `expected`

## Additional Notes
* This autotester uses a custom version of `Wrapper_tb.v` and can be found in the `test_files` directory. This version only outputs failed registers and a final pass/fail message. GTKWave is also disabled. 
* Make sure there is a new line at the end of all exp files in the `test_files/verification_files` directory. 
* There is a work-in-progress automatic OS detection function in `helper_scripts/asm_compiler.py`. It didn't work for detecting between Apple Silicon and Intel Macs. Another possible solution is to compile the source files for the assembler dynamically. 
* Windows version of the script is currently untested. Errors may arise from the FileList generation, which uses a different syntax on Windows.