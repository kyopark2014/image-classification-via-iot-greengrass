from logging import INFO, StreamHandler, getLogger
from sys import stdout
from cv2 import VideoCapture, destroyAllWindows, imdecode, imread, resize
from dlr import DLRModel
from numpy import argsort, frombuffer, fromstring, load, uint8
from os import environ, path
from ast import literal_eval

logger = getLogger()
#handler = StreamHandler(stdout)
#logger.setLevel(INFO)
#logger.addHandler(handler)

IMAGE_DIR = './images'
SCORE_THRESHOLD = 0.3
MAX_NO_OF_RESULTS = 5
SHAPE = (224, 224)

# Read synset file
MODEL_DIR = './model'
LABELS = path.join(MODEL_DIR, "synset.txt")
with open(LABELS, "r") as f:
    synset = literal_eval(f.read())

dlr_model = DLRModel(MODEL_DIR, 'cpu')

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

def predict_from_image(image_data):
    try:
        # Run DLR to perform inference with DLC optimized model
        model_output = dlr_model.run(image_data)

        probabilities = model_output[0][0]
        sort_classes_by_probability = argsort(probabilities)[::-1]
        for i in sort_classes_by_probability[: MAX_NO_OF_RESULTS]:
            if probabilities[i] >= SCORE_THRESHOLD:
                result = {"Label": str(synset[i]), "Score": str(probabilities[i])}
                logger.info("result: {}".format(result))
    except Exception as e:
        logger.error("Exception occured during prediction: {}".format(e))

def main():
    image = load_image(path.join(IMAGE_DIR, 'cat.jpeg'))
    cvimage = resize(image, SHAPE)

    if cvimage is not None:
        predict_from_image(cvimage)
        return
    else:
        logger.error("Unable to capture an image using camera")
        exit(1)

if __name__ == '__main__':
    main()