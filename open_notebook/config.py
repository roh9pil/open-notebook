import os

# ROOT DATA FOLDER
DATA_FOLDER = "./data"

# LANGGRAPH CHECKPOINT FILE
sqlite_folder = f"{DATA_FOLDER}/sqlite-db"
os.makedirs(sqlite_folder, exist_ok=True)
LANGGRAPH_CHECKPOINT_FILE = f"{sqlite_folder}/checkpoints.sqlite"

# UPLOADS FOLDER
UPLOADS_FOLDER = f"{DATA_FOLDER}/uploads"
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

# TIKTOKEN CACHE FOLDER
TIKTOKEN_CACHE_DIR = f"{DATA_FOLDER}/tiktoken-cache"
os.makedirs(TIKTOKEN_CACHE_DIR, exist_ok=True)

# OPENAI COMPATIBLE TOKEN USAGE
# Controls whether to measure token usage for OpenAI compatible models
# Default: True (measure usage)
# Set to False to disable usage measurement (e.g., for local models or performance)
OPENAI_COMPATIBLE_TOKEN_USAGE = os.getenv("OPENAI_COMPATIBLE_TOKEN_USAGE", "true").lower() == "true"
