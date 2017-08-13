import logging
import time

logger = logging.getLogger(__name__)

def get_config(config_file_name):
    lines = {}
    with open(config_file_name) as file_handle:
        logger.debug("{}:: Config file {} found".format(time.time(), config_file_name))

        for line in file_handle:
            if line[0] == '#':
                continue
            line = [words.strip(' \n') for words in line.split(':')]
            lines[line[0]] = line[1]
    if lines != {}:
        return lines

    logger.error("{} Config file {} not found".format(int(time.time()), config_file_name))

