############# bot-hosting-wrapper files
from .about import *
from .interactive import *
from .panel import *
############# bot-hosting-wrapper files
import logging

LOGGING_ENABLED = True  # You can later set this from your own program (e.g. bot-hosting-wrapper.LOGGING_ENABLED = True)

if LOGGING_ENABLED:
    logging.basicConfig(level=logging.INFO)
    logging.info("Package 'bot_hosting_wrapper' has been initialized.")