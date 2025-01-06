import logging
import logging.config
from os import path
import os
import uvicorn


log_config = uvicorn.config.LOGGING_CONFIG
LOG_LEVEL = os.getenv("LOG_LEVEL", default="DEBUG")
log_config["formatters"]["access"]["fmt"] = "%(levelname)s:  %(asctime)s - %(name)s -  module %(module)s : Line %(lineno)d - %(message)s"

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
log = logging.getLogger('home-automation')
log.setLevel(LOG_LEVEL)