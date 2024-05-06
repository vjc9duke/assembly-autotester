import default_values as dv
from datetime import datetime
import os

class Logger:
    """
    Logging class that logs messages to the terminal or a file.
    """

    priority_dict = {"INFO": 0, "IVERILOG": 10, "WARN": 20, "ERROR": 30, "NONE": 5000}

    def setup(log_level="INFO", output_destination="TERM", rolling=True, folder_path=dv.LOG_DIR):
        Logger.log_level = Logger.priority_dict[log_level.upper()]
        Logger.output_destination = output_destination.upper()
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if(rolling):
            Logger.delete_old_files(folder_path)
    
        # Construct file name with today's date
        Logger.file_path = os.path.join(folder_path, f"log_{curr_time}.txt")

        # Create the file
        with open(Logger.file_path, 'w') as file:
            file.write("Log output for run at " + curr_time + "\n")

    def delete_old_files(directory):
        try:
            # Get a list of all files in the directory along with their modification times
            files = [(os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f))) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            
            # Sort the files based on modification times
            files.sort(key=lambda x: x[1])

            # Keep the four most recent files and delete the rest
            files_to_delete = files[:-4]
            for file, _ in files_to_delete:
                os.remove(file)
            
        except OSError as e:
            print(f"Logging Error: {e}")
        

    def info(message):
        if Logger.log_level <= Logger.priority_dict["INFO"]:
            Logger._output_message("INFO", message)

    def iverilog(message):
        if Logger.log_level <= Logger.priority_dict["IVERILOG"]:
            Logger._output_message("IVERILOG", message)
        
    def warn(message):
        if Logger.log_level <= Logger.priority_dict["WARN"]:
            Logger._output_message("WARN", message)

    def error(message):
        if Logger.log_level <= Logger.priority_dict["ERROR"]:
            Logger._output_message("ERROR", message)

    def _output_message(level, message):
        formatted_message = f"[{level}] {message}"
        if Logger.output_destination == "TERM":
            print(formatted_message)
        elif Logger.output_destination == "FILE":
            if Logger.file_path:
                with open(Logger.file_path, "a") as file:
                    file.write(formatted_message + "\n")
            else:
                raise ValueError("File path must be provided for file output.")
        else:
            raise ValueError("Invalid output destination. Choose 'TERM' or 'FILE'.")

# Example usage:
if __name__ == "__main__":
    Logger.setup(log_level="INFO", output_destination="TERM")
    Logger.info("This is an information message")
    Logger.iverilog("This is iverilog output")
    Logger.warn("This is a warning message")
    Logger.error("This is an error message")
