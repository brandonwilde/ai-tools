import base64
from functools import wraps
import os
import string
import time


def log_time(func):
    '''
    Print the time it takes for an LLM call to process.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f'Response took {end - start:.2f} seconds.')
        return result
    return wrapper


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


def filenamify(s: str) -> str:
    '''
    Remove a string's punctuation, replace spaces with underscores, and put in lowercase.
    '''
    character_map = str.maketrans(' ','_', string.punctuation)
    return s.translate(character_map).lower()


def encode_image(image_path):
    '''
    Encode an image as base64.
    '''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def countdown(seconds):
    '''
    Print a countdown timer.
    '''
    for i in range(seconds, 0, -1):
      print(f"\r{i} seconds remaining...", end='', flush=True)
      time.sleep(1)
    print("\r0 seconds remain.", flush=True)