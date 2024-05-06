import os
import shutil

def delete_old_files(directory, num_to_keep=5):
    try:
        # Get a list of all files in the directory along with their modification times
        files = [(os.path.join(directory, f), os.path.getmtime(os.path.join(directory, f))) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Sort the files based on modification times
        files.sort(key=lambda x: x[1])

        # Keep the four most recent files and delete the rest
        files_to_delete = files[:-(num_to_keep-1)]
        for file, _ in files_to_delete:
            os.remove(file)
        
    except OSError as e:
        print(f"Failed to delete files: {e}")  # circular import prevents the use of Logger here

def delete_old_folders(directory, num_to_keep=5):
    try:
        # Get a list of all directories in the specified directory
        directories = [(os.path.join(directory, d), os.path.getmtime(os.path.join(directory, d))) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        
        # Sort the directories based on modification times
        directories.sort(key=lambda x: x[1])

        # Keep the num_to_keep most recent directories and delete the rest
        directories_to_delete = directories[:-(num_to_keep-1)]
        for folder, _ in directories_to_delete:
            shutil.rmtree(folder)
        
    except OSError as e:
        print(f"Failed to delete folders: {e}")
