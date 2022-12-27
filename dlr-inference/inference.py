from logging import INFO, StreamHandler, getLogger
from sys import stdout
from dlr import DLRModel
from numpy import argsort, frombuffer, fromstring, load, uint8
from os import environ, path
from ast import literal_eval

SCORE_THRESHOLD = 0.3
MAX_NO_OF_RESULTS = 5
MODEL_DIR = '/tmp/images/'
logger = getLogger()
handler = StreamHandler(stdout)
logger.setLevel(INFO)
logger.addHandler(handler)

dlr_model = DLRModel(MODEL_DIR, 'cpu')

LABELS = path.join(MODEL_DIR, "synset.txt")

# Read synset file
with open(LABELS, "r") as f:
    synset = literal_eval(f.read())

try:
    # Run DLR to perform inference with DLC optimized model
    model_output = dlr_model.run(image_data)

    probabilities = model_output[0][0]
    sort_classes_by_probability = argsort(probabilities)[::-1]
    for i in sort_classes_by_probability[: MAX_NO_OF_RESULTS]:
        if probabilities[i] >= SCORE_THRESHOLD:
            result = {"Label": str(synset[i]), "Score": str(probabilities[i])}

except Exception as e:
    logger.error("Exception occured during prediction: {}".format(e))




