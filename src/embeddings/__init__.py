import os
import logging
from transformers import logging as hf_logging

os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

hf_logging.set_verbosity_error()
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
