import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseManager:
    def __init__(self):
        # 1. Initialize MongoDB Connection
        # We use the URL from your .env file
        self.client = MongoClient(os.getenv("MONGO_URL"))
        
        # 2. Define the Master Database Name
        # This DB will hold the global metadata
        self.master_db_name = os.getenv("MASTER_DB_NAME", "master_org_db")
        self.master_db = self.client[self.master_db_name]

    def get_master_collection(self):
        """
        Returns the collection that stores metadata about all organizations.
        This corresponds to the 'Master Database' requirement.
        """
        return self.master_db["organization_metadata"]

    def get_org_collection(self, org_name: str):
        """
        Returns the specific collection for a given organization.
        Format: org_<organization_name>
        
        Note: In MongoDB, collections are 'lazy'. The collection is 
        technically created only when data is first written to it.
        This satisfies the 'Dynamically create a new Mongo collection' requirement.
        """
        # Sanitize org_name to ensure valid collection name (remove spaces, lowercase)
        safe_name = org_name.strip().lower().replace(" ", "_")
        collection_name = f"org_{safe_name}"
        
        # We store these collections in the SAME database as master for simplicity,
        # but logically they are isolated "tenant" data.
        return self.master_db[collection_name]

# Create a global instance to be used throughout the app
db_manager = DatabaseManager()