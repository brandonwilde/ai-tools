from datetime import datetime
import os
import re
import time

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import requests


AZURE_API_KEY = os.environ.get('AZURE_API_KEY')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')

def send_to_ocr(filepath):
  read_url = f"{AZURE_ENDPOINT}/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2023-07-31"

  with open(filepath, "rb") as f:
    image = f.read()

  return requests.post(
    url=read_url,
    headers={
      "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
      "Content-Type": "image/jpeg",
    },
    data=image
  )


def is_running(response_json):
  if response_json['status'] == 'running':
    return True
  else:
    return False


def countdown(seconds):
    for i in range(seconds, 0, -1):
      print(f"\r{i} seconds remaining...", end='', flush=True)
      time.sleep(1)
    print("\r0 seconds remain.", flush=True)




def read_file(filepath):
  
    RATE_LIMIT_REACHED = True

    def check_for_error(response_json):
        if 'error' in response_json:
            error = response_json['error']
            if error['code'] == '429':
                wait_time = int(re.search('retry after (\d+) second', error['message'])[1])
                print(f"Rate limit reached. Will resume after {wait_time} seconds.")
                countdown(wait_time)
                return True
            else:
                print("Error in OCR response:", error)
                raise Exception(error['message'])

    while RATE_LIMIT_REACHED:
        RATE_LIMIT_REACHED = False # reset

        print(f"Sending {filepath.split('/')[-1]} to Azure...")
        response = send_to_ocr(filepath)

        if not 200 <= response.status_code < 300:
            if check_for_error(response.json()):
                RATE_LIMIT_REACHED = True
                continue

        result_url = response.headers['Operation-Location']

        still_running = True
        while still_running:
            ocr_response = requests.get(
                url=result_url,
                headers={
                "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
                },
            ).json()

            if check_for_error(ocr_response):
                RATE_LIMIT_REACHED = True
                continue

        still_running = is_running(ocr_response)
        print("Job is still running. Checking for another status update...")


    if not ocr_response['status'] == 'succeeded':
        print(ocr_response)
        raise Exception("Unexpected status:", ocr_response['status'])

    pages = ocr_response['analyzeResult']['pages']
    result = ""
    for page in pages:
        for line in page['lines']:
            result += line['content'] + '\n'
  
    return result


def read_sdk(filename):
    document_analysis_client = DocumentAnalysisClient(
        endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_API_KEY)
    )

    with open(filename, 'rb') as f:
        file = f.read()

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-read", file)
    result = poller.result()
    
    return result


def batch_read(folder, files):
    results = []
    for file in files:
        filepath = os.path.join(folder, file)
        print(f"Submitting {file} for OCR.")
        file_text = read_file(filepath)
        results.append((file, file_text))


    for (filename, text) in results:
        with open("texts.txt", "a") as f:
            f.write(filename + '\n')
            f.write(text + '\n\n')

    results.sort(
    key=lambda x:datetime.strptime(
        re.search('\d?\d:\d\d', x[1]).group(),
        '%H:%M'
    )) # sort by timestamp - doesn't work if time not in every image

    for (filename, text) in results:
        with open("texts-sorted.txt", "a") as f:
            f.write(filename + '\n')
            f.write(text + '\n\n')


# folder = "/path/to/images"
# files = sorted([i for i in os.listdir(folder) if any(x in i for x in ['png', 'jpeg'])])


# batch_read(folder, files)

if __name__ == "__main__":
    file = "IMG_20240210_115126.jpg"
    content = read_sdk(file)
    with open(file.replace('.jpg', '.txt'), 'w') as f:
        f.write(content)