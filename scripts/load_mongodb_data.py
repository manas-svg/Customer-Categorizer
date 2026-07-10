import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / "src" / "cloud_storage" / ".env", override=True)

sys.path.append(str(PROJECT_ROOT))

from src.configuration.mongo_db_connection import MongoDBClient
from src.constant.database import DATABASE_NAME


def main() -> None:
    dataset_path = PROJECT_ROOT / "notebooks" / "marketing_campaign.csv"
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    df = pd.read_csv(dataset_path, sep="\t")
    client = MongoDBClient(database_name=DATABASE_NAME)
    db = client.database
    collection = db["customer_segmentation"]

    collection.delete_many({})
    records = df.to_dict(orient="records")
    collection.insert_many(records)

    print(f"Inserted {len(records)} documents into {db.name}.{collection.name}")
    print("Sample document:")
    print(collection.find_one())


if __name__ == "__main__":
    main()
