import argparse
import logging
from typing import List

from database_manager import DatabaseManager

class DataTransformer:
    def __init__(self, database_path: str, query_directory: str):
        """Initialize DataTransformer with database and query paths"""
        self.database_path = database_path
        self.query_directory = query_directory
        self.db_manager = DatabaseManager(database_path, query_directory)
        logging.getLogger().setLevel(logging.INFO)

    def transform_data(self) -> None:
        """Execute transformation queries in sequence"""
        try:
            # Get all transformation queries
            query_paths = self.db_manager.collect_query_paths()
            
            # Connect to database
            self.db_manager.connect()
            
            # Execute each transformation query
            for query_path in query_paths:
                query = self.db_manager.read_query(query_path)
                self.db_manager.execute_query(query)
                logging.info(f"Executed transformation query from {query_path}")
                
        except Exception as e:
            logging.error(f"Error during transformation: {str(e)}")
            raise
        finally:
            self.db_manager.close()

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="CLI for Data Transformation")
    parser.add_argument(
        "--database_path", 
        type=str, 
        required=True, 
        help="Path to the DuckDB database"
    )
    parser.add_argument(
        "--query_directory",
        type=str,
        required=True,
        help="Directory containing SQL transformation queries",
    )

    # Parse arguments and run transformation
    args = parser.parse_args()
    
    transformer = DataTransformer(
        database_path=args.database_path,
        query_directory=args.query_directory
    )
    transformer.transform_data()


if __name__ == "__main__":
    main()