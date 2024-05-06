import default_values as dv
from datetime import datetime
import os

"""
Logging class that logs messages to the terminal or a file.
"""
class Logger:
    _instance = None
    priority_dict = {"INFO": 0, "IVERILOG": 10, "WARN": 20, "ERROR": 30}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.setup()
        return cls._instance

    def setup(self, log_level="INFO", output_destination="TERM", folder_path=dv.LOG_DIR):
        self.log_level = Logger.priority_dict[log_level.upper()]
        self.output_destination = output_destination.upper()
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        curr_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
        # Construct file name with today's date
        self.file_path = os.path.join(folder_path, f"log_{curr_time}.txt")

        # Create the file
        with open(self.file_path, 'w') as file:
            file.write("Log output for run at " + curr_time + "\n")


    def info(self, message):
        if self.log_level <= Logger.priority_dict["INFO"]:
            self._output_message("INFO", message)

    def iverilog(self, message):
        if self.log_level <= Logger.priority_dict["IVERILOG"]:
            self._output_message("IVERILOG", message)
        
    def warn(self, message):
        if self.log_level <= Logger.priority_dict["WARN"]:
            self._output_message("WARN", message)

    def error(self, message):
        if self.log_level <= Logger.priority_dict["ERROR"]:
            self._output_message("ERROR", message)

    def _output_message(self, level, message):
        formatted_message = f"[{level}] {message}"
        if self.output_destination == "TERM":
            print(formatted_message)
        elif self.output_destination == "FILE":
            if self.file_path:
                with open(self.file_path, "a") as file:
                    file.write(formatted_message + "\n")
            else:
                raise ValueError("File path must be provided for file output.")
        else:
            raise ValueError("Invalid output destination. Choose 'TERM' or 'FILE'.")

# Example usage:
if __name__ == "__main__":
    logger = Logger()
    logger.setup(log_level="INFO", output_destination="FILE")
    logger.info("This is an information message")
    logger.iverilog("This is iverilog output")
    logger.warn("This is a warning message")
    logger.error("This is an error message")
