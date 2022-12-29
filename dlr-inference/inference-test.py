from logging import INFO, StreamHandler, getLogger
from sys import stdout
from cv2 import imread
from numpy import load
from os import path
from ast import literal_eval
import os
import traceback
import json

import dlr
from dlr.counter.phone_home import PhoneHome                             
PhoneHome.disable_feature()   

logger = getLogger()
handler = StreamHandler(stdout)
logger.setLevel(INFO)
logger.addHandler(handler)

IMAGE_DIR = f'{os.getcwd()}/images'
print('IMAGE_DIR:', IMAGE_DIR)

def load_image(image_path):
    # Case insenstive check of the image type.
    img_lower = image_path.lower()
    if (
        img_lower.endswith(
            ".jpg",
            -4,
        )
        or img_lower.endswith(
            ".png",
            -4,
        )
        or img_lower.endswith(
            ".jpeg",
            -5,
        )
    ):
        try:
            image_data = imread(image_path)
        except Exception as e:
            logger.error(
                "Unable to read the image at: {}. Error: {}".format(image_path, e)
            )
            exit(1)
    elif img_lower.endswith(
        ".npy",
        -4,
    ):
        image_data = load(image_path)
    else:
        logger.error("Images of format jpg,jpeg,png and npy are only supported.")
        exit(1)
    return image_data

def main():
    image = load_image(path.join(IMAGE_DIR, 'cat.jpeg'))

    try:
        results = handler(image,"")          
        print('result: ' + json.dumps(results['body']))
    except:
        traceback.print_exc()
        
if __name__ == '__main__':
    main()
