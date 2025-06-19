import subprocess
import os

import internal

def get_data(url: str, output_file: str):
    folder_path = './data/'
    output_path = os.path.join(folder_path, output_file)

    # Make sure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Run curl
    subprocess.run(["curl", "-L", url, "-o", output_path])

def call_api_get(url: str, output_file: str):
    output_path = './api_data/'
    api_key = internal.get_internal()

    cmd = [
        "curl", "-L", "-X", "GET",
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Accept: application/json",
        "-o", output_path + output_file,
        url
    ]

    subprocess.run(cmd)
