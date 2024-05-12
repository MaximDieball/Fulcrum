import os

def list_folders(directory):
    if os.path.exists(directory):
        print("Folders inside", directory)
        for folder in os.listdir(directory):
            folder_path = os.path.join(directory, folder)
            if os.path.isdir(folder_path):
                print(folder_path)
    else:
        print("Directory does not exist.")

# Example usage
directory = "C:\\Program Files"
list_folders(directory)
