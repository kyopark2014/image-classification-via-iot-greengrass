from logging import INFO, StreamHandler, getLogger
import time

logger = getLogger()
logging_handler = StreamHandler(stdout)
logger.setLevel(INFO)
logger.addHandler(logging_handler)

def main():
    while True:
        print('Hello')
        time.sleep(10)

if __name__ == '__main__':
    main()
