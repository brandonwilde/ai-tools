import os


def increment_file_name(file_path):
    '''
    Increment the file name if it already exists.
    '''
    version = 1
    base, ext = os.path.splitext(file_path)
    while os.path.exists(file_path):
        version += 1
        file_path = f"{base}_v{version}{ext}"

    return file_path