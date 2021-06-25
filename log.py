import logging

# create logger
logger = logging.getLogger('appLog')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler and set level to debug
fh = logging.FileHandler('appLogs',encoding='utf-8',mode='a')
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)

def writeLog(msg, level):
    if level == "DEBUG":
        logger.debug(msg)
    if level == "INFO":
        logger.info(msg)
    if level == "WARNING":
        logger.warning(msg)
    if level == "ERROR":
        logger.error(msg)

