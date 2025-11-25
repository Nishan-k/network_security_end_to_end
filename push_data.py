import pandas as pd
import json
import os
import sys
from dotenv import load_dotenv
import certifi
import numpy as np
import pymongo
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException


load_dotenv()


mongo_uri = os.getenv("MONGO_DB_URL")

ca = certifi.where()

