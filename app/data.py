from os import getenv

import pymongo
from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
import pandas as pd
from pandas import DataFrame
from pymongo import MongoClient
from tqdm import tqdm

# Acquiring the connection link to MongoDB and connecting
load_dotenv('.env')
uri = getenv('DB_URL')

client = MongoClient(uri, ssl=True)

# Setting up the database
db = client.monsters
collection = db.monster_data

class Database:
    """
    A class to interact with the MongoDB database for storing monster data.
    """

    def __init__(self):
        """
        Initializes the Database object.
        """
        self.collection = collection

    def seed(self, amount=2048):
        """
        Seeds the database with a specified number of monster records.

        Args:
            amount (int): The number of monster records to seed. Default is 2048.
        """
        count = 0

        for i in tqdm(range(amount)):
            res = Monster().to_dict()
            self.collection.insert_one(res)
            count += 1

            if count == amount:
                break

    def reset(self):
        """
        Resets the database by deleting all monster records.
        """
        self.collection.delete_many({})

    def count(self) -> int:
        """
        Returns the count of monster records in the database.

        Returns:
            int: The count of monster records.
        """
        doc_count = self.collection.count_documents({})
        return doc_count

    def dataframe(self) -> DataFrame:
        """
        Retrieves the monster records from the database and returns them as a pandas DataFrame.

        Returns:
            DataFrame: A DataFrame containing the monster records.
        """
        docs = list(self.collection.find())
        df = pd.DataFrame(docs)
        df = df.drop("_id", axis=1)
        self.df = df
        return df

    def html_table(self) -> str:
        """
        Generates an HTML table representation of the monster records stored in the database.

        Returns:
            str: The HTML table representation of the monster records.
        """
        if hasattr(self, 'df'):
            table = self.df.to_html()
            return table
        else:
            return 'Dataframe Not Generated Yet'

if __name__ == '__main__':
    db = Database()
    db.reset()
    db.seed(2048)
    #db.dataframe()
