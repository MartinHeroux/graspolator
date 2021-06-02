import os

def get_filename_list(directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filenames.append(filename)
    return filenames

def get_directory_list(directory):
    directories = []
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            directories.append(directory)
    return directories