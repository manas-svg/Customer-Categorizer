import os
import sys
from pathlib import Path

import certifi
import pymongo
from dotenv import find_dotenv, load_dotenv

from src.constant.database import DATABASE_NAME
from src.constant.env_variable import MONGODB_URL_KEY
from src.exception import CustomerException

ca = certifi.where()


class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                self._load_environment_variables()
                mongo_db_url = (
                    os.getenv(MONGODB_URL_KEY)
                    or os.getenv("MONGODB_URL")
                    or os.getenv("MONGODB_URI")
                )
                if not mongo_db_url:
                    raise Exception(
                        f"Environment key: {MONGODB_URL_KEY} is not set. Checked MONGO_DB_URL, MONGODB_URL, and MONGODB_URI."
                    )
                mongo_db_url = mongo_db_url.strip().strip("'\"")
                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tlsCAFile=ca,
                    serverSelectionTimeoutMS=10000,
                )
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise CustomerException(e, sys)

    @staticmethod
    def _load_environment_variables() -> None:
        load_dotenv(find_dotenv(usecwd=True), override=False)

        project_root = Path(__file__).resolve().parents[2]
        candidate_files = [
            project_root / ".env",
            project_root / "src" / "cloud_storage" / ".env",
            Path.cwd() / ".env",
        ]

        for env_file in candidate_files:
            if env_file.exists():
                load_dotenv(env_file, override=False)
if __name__ == "__main__":
    mongo = MongoDBClient()
    print("MongoDB Connected Successfully")