import json
import os
import logging
from datetime import datetime

DB_FILE = "data/database.json"


logging.basicConfig(filename="server.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

"""config:[
    
]"""