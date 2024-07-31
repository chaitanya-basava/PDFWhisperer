import os
import time


directory = "./sessions/"
if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"Directory created: {directory}")


def delete_old_files(seconds_old):
    # Get the current time
    current_time = time.time()

    # Calculate the time threshold in seconds
    time_threshold = current_time - seconds_old

    # Iterate through all files in the specified directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Get the last modified time of the file
            file_modified_time = os.path.getmtime(file_path)

            # Check if the file is older than the threshold
            if file_modified_time < time_threshold:
                try:
                    # Delete the file
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
