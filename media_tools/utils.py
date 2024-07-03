import base64
import os
import time


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


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def countdown(seconds):
    for i in range(seconds, 0, -1):
      print(f"\r{i} seconds remaining...", end='', flush=True)
      time.sleep(1)
    print("\r0 seconds remain.", flush=True)