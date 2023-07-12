import subprocess
from pathlib import Path
import os
import re
import requests
import shutil
import cv2
import time
import glob
import datetime

# Set this when user have signed up
USER_ID = 3
DISEASES_DICT = {
    '1': "Tip Burn",
    '2': "Brown Spots",
    '3': "Yellowing and Wilting",
    '4': "Gray White",
    '5': "Healthy"
}

def take_arduino_actions():
    # write arduino steps here
    # In progress
    a=10


def send_notification(current_dir, result_folder_path,first_line,largest_number):

    url = "https://nft-hydrophonic-delta.vercel.app/image-diseases-upload"
    print('Class ID:', first_line)
    payload = {
        'diseases_type': DISEASES_DICT[first_line[-1]],
        'user_id': USER_ID
    }
    
    with open(current_dir + f'/test-model/capture-image-{largest_number}.jpg', 'rb') as image_file:
        image_data = image_file.read()

    current_time = datetime.datetime.now()
    files = [
        ('diseases-image', (f'notification-image-{current_time.strftime("%Y%m%d%H%M%S")}.jpg', image_data, 'image/jpeg'))
    ]

    
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
        


def main():
    current_dir = os.getcwd()
    result_folder_path = current_dir+'/test-model'

    # Get a list of all "doc-*.txt" files
    txt_files = glob.glob('test-model/detection-info-*.txt')
    print('Files:', txt_files)


    # Extract the number from each filename and find the file with the maximum number
    latest_file = max(txt_files, key=lambda filename: int(os.path.splitext(os.path.basename(filename))[0].split('-')[2]))
    print("Latest File: ",latest_file)
    largest_number = int(os.path.splitext(os.path.basename(latest_file))[0].split('-')[2])

    # Read and print the content of the latest file
    with open(latest_file, 'r') as file:
        first_line = file.readline().strip().split()
        print("First Line -> : ",first_line)

        if(len(first_line) != 0):
            if(first_line[-1] != '5'):
                send_notification(current_dir, result_folder_path,first_line,largest_number)
            else:
                print("Healthy")
        else:
            print("File Empty")

def delete_folder_if_exists(path):
    if os.path.exists(path) and os.path.isdir(path):
        try:
            shutil.rmtree(path)
            print(f'Successfully deleted the folder: {path}')
        except Exception as e:
            print(f'Failed to delete the folder: {path}. Reason: {e}')
    else:
        print(f'The folder: {path} does not exist')


if __name__ == '__main__':
    main()
    
