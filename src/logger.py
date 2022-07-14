import logging

logging.basicConfig(filename='syllabify.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
