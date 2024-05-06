import subprocess
from logger import Logger
import sys
import os
import shutil

def assemble_all(asb_dir="test_files/assembler", asm_dir='test_files/assembly_files', mem_dir="test_files/mem_files", os_name="Linux"):
    if not os.path.exists(asm_dir):
        Logger.error(f"Could not find directory '{asm_dir}' for assembly files.")
        sys.exit(1)

    if not os.path.isdir(asm_dir):
        Logger.error(f"'{asm_dir}' is not a directory.")
        sys.exit(1)

    # Create mem dir if it does not exist
    if not os.path.exists(mem_dir):
        os.makedirs(mem_dir)
        Logger.warn(f"'{mem_dir}' did not exist. Directory created.")

    # Clear previous files in mem dir
    for filename in os.listdir(mem_dir):
        file_path = os.path.join(mem_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except OSError as e:
            Logger.warn(f"Error deleting mem file '{file_path}'. Error: {e}")

    for filename in os.listdir(asm_dir):
        path = os.path.join(asm_dir, filename)
        if os.path.isfile(path) and filename.endswith('.s'):
            assemble(file_path=path, canonical_name=os.path.splitext(filename)[0], asb_dir=asb_dir, asm_dir=asm_dir, mem_dir=mem_dir, os_name=os_name)

def assemble(file_path, canonical_name, asb_dir, asm_dir, mem_dir, os_name):

    # Path to the assembler executable
    # TODO: null check
    assembler_path = f"{asb_dir}/asm_{os_name.upper()}"

    # Command to run the assembler
    command = [assembler_path, file_path]

    try:
        # Run the assembler
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Move mem file to correct location
        mem_file_path = os.path.join(asm_dir, canonical_name + ".mem")
        moved_to = os.path.join(mem_dir, canonical_name + ".mem")
        shutil.move(mem_file_path, moved_to)

        Logger.info(f"Assembly successful for {file_path}. Output written to {moved_to}.")
    except subprocess.CalledProcessError as e:
        Logger.warn(f"Assembler failed to execute for {file_path}. Error: {e}")
    except IOError as e:
        Logger.warn(f"Error writing to memory file for {file_path}. Error: {e}")

if __name__ == "__main__":
    Logger.setup(log_level="INFO", output_destination="TERM")
    assemble_all(os_name="MacM1")