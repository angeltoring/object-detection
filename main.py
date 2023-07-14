import subprocess
import cv2
import os
import shutil

def main():

    folder_path = 'test-model'
    print("**",os.getcwd())
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    folder_path = '/yolov5/runs/detect'

    # Remove the entire directory
    shutil.rmtree(os.getcwd()+folder_path)
    # Recreate the directory
    os.makedirs(os.getcwd()+folder_path)

    command = [
        'python', 'yolov5/detect.py',
        '--weights', 'yolov5/best.pt',
        '--conf', '0.50',
        '--max-det', '1',
        '--source', '0',
        '--frame_saved_interval', '13800' #every 3hr 50 min
    ]

    result = subprocess.run(command, check=True)
    if result.returncode == 0:
        print("Detection completed successfully")
    else:
        print("Detection failed")
        
if __name__ == "__main__":
    main()
