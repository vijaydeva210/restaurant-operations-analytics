import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()

uri = os.getenv("COGNODB_URI")
username = os.getenv("COGNODB_USERNAME")
password = os.getenv("COGNODB_PASSWORD")


driver = GraphDatabase.driver(
    uri,
    auth=(username, password)
)


def run_query(query, parameters=None):
    try:
        with driver.session() as session:
            result = session.run(query, parameters)
            return result.data()

    except Exception as error:
        print(f"Database error: {error}")
        raise ConnectionError(
            "Unable to connect to the graph database."
        )