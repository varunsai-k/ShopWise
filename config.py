from dotenv import load_dotenv
load_dotenv()
import os

GOOGLE_API_KEY=os.environ["GOOGLE_API_KEY"]
LANGSMITH_API_KEY=os.environ["LANGSMITH_API_KEY"]
LANGSMITH_TRACING=os.environ["LANGSMITH_TRACING"]
DB_PATH=os.environ["DB_PATH"]
