from typing import List
import os
import argparse
import logging

from duckdb import DuckDBPyConnection
import duckdb as ddb


class DatabaseManager:
    def __init__(self, database_path: str, ddl_query_parent_dir: str = None):
        self.database_path = database_path
        self.ddl_query_parent_dir = ddl_query_parent_dir
        self.connection = None
        logging.getLogger().setLevel(logging.INFO)

    def connect(self) -> DuckDBPyConnection:
        """Connect to the database"""
        logging.info(f"Connecting to database at {self.database_path}")
        self.connection = ddb.connect(self.database_path)
        self.connection.sql("""
            SET s3_access_key_id='';
            SET s3_secret_access_key='';
            SET s3_region='';
            """)
        return self.connection

    def close(self) -> None:
        """Close the database connection"""
        if self.connection:
            logging.info("Closing database connection")
            self.connection.close()
            self.connection = None

    def collect_query_paths(self) -> List[str]:
        """Collect all SQL query paths"""
        sql_files = []
        for root, _, files in os.walk(self.ddl_query_parent_dir):
            for file in files:
                if file.endswith(".sql"):
                    file_path = os.path.join(root, file)
                    sql_files.append(file_path)
        
        logging.info(f"Found {len(sql_files)} sql scripts at location {self.ddl_query_parent_dir}")
        return sorted(sql_files)

    @staticmethod
    def read_query(path: str) -> str:
        """Read SQL query from file"""
        with open(path, "r") as f:
            query = f.read()
        return query

    def execute_query(self, query: str) -> None:
        """Execute SQL query"""
        if self.connection:
            self.connection.execute(query)

    def setup(self) -> None:
        """Setup the database"""
        query_paths = self.collect_query_paths()
        self.connect()

        for query_path in query_paths:
            query = self.read_query(query_path)
            self.execute_query(query)
            logging.info(f"Executed query from {query_path}")
        
        self.close()

    def destroy(self) -> None:
        """Destroy the database"""
        self.close()
        if os.path.exists(self.database_path):
            os.remove(self.database_path)
            logging.info(f"Destroyed database at {self.database_path}")


def main():
    parser = argparse.ArgumentParser(description="CLI tool to setup or destroy a database.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create", action="store_true", help="Create the database")
    group.add_argument("--destroy", action="store_true", help="Destroy the database")

    parser.add_argument("--database-path", type=str, help="Path to the database")
    parser.add_argument("--ddl-query-parent-dir", type=str, help="Path to the parent directory of the ddl queries")

    args = parser.parse_args()
    
    db_manager = DatabaseManager(
        database_path=args.database_path,
        ddl_query_parent_dir=args.ddl_query_parent_dir
    )

    if args.create:
        db_manager.setup()
    elif args.destroy:
        db_manager.destroy()


if __name__ == "__main__":
    main()