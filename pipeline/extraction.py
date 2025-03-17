"""
Example usage: python extraction.py --locations_file_path ../location.json --start_date 2024-01 --end_date 2025-01 --database_path ../air_quality.db --extract_query_template_path ../sql/dml/raw/0_raw_air_quality_insert.sql --source_base_path s3://openaq-data-archive/records/csv.gz
"""
import argparse
import json
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import List

from duckdb import IOException, DuckDBPyConnection
from jinja2 import Template

from database_manager import DatabaseManager

class DataExtractor:
    def __init__(
        self,
        locations_file_path: str,
        start_date: str,
        end_date: str,
        database_path: str,
        extract_query_template_path: str,
        source_base_path: str
    ):
        self.locations_file_path = locations_file_path
        self.start_date = start_date
        self.end_date = end_date
        self.database_path = database_path
        self.extract_query_template_path = extract_query_template_path
        self.source_base_path = source_base_path
        self.db_manager = DatabaseManager(database_path)
        self.data_file_path_template = "locationid={{location_id}}/year={{year}}/month={{month}}/*"
        
    def read_location_ids(self) -> List[str]:
        """Read location IDs from JSON file"""
        with open(self.locations_file_path, "r") as f:
            location = json.load(f)
        return [str(id) for id in location.keys()]

    def compile_data_file_paths(self, location_ids: List[str]) -> List[str]:
        """Generate list of data file paths"""
        start_date = datetime.strptime(self.start_date, "%Y-%m")
        end_date = datetime.strptime(self.end_date, "%Y-%m")

        data_file_paths = []
        for location_id in location_ids:
            index_date = start_date
            while index_date <= end_date:
                data_file_path = Template(self.data_file_path_template).render(
                    location_id=location_id,
                    year=str(index_date.year),
                    month=str(index_date.month).zfill(2),
                    day=str(index_date.day).zfill(2)
                )
                data_file_paths.append(data_file_path)
                index_date += relativedelta(months=1)
        return data_file_paths

    def compile_data_file_query(self, data_file_path: str, extract_query_template: str) -> str:
        """Compile query for data file extraction"""
        return Template(extract_query_template).render(
            data_file_path=f"{self.source_base_path}/{data_file_path}"
        )

    def extract_data(self):
        """Main extraction process"""
        location_ids = self.read_location_ids()
        data_file_paths = self.compile_data_file_paths(location_ids)
        extract_query_template = self.db_manager.read_query(self.extract_query_template_path)
        
        connection = self.db_manager.connect()

        for data_file_path in data_file_paths:
            logging.info(f"Extracting data from {data_file_path}")
            query = self.compile_data_file_query(data_file_path, extract_query_template)

            try:
                self.db_manager.execute_query(query)
                logging.info(f"Extracted data from {data_file_path}!")
            except IOException as e:
                logging.warning(f"Could not find data from {data_file_path}: {e}")
        
        self.db_manager.close()

def main():
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(description="CLI for ELT Extraction")
    parser.add_argument(
        "--locations_file_path",
        type=str,
        required=True,
        help="Path to the locations JSON file",
    )
    parser.add_argument(
        "--start_date",
        type=str,
        required=True,
        help="Start date in YYYY-MM format"
    )
    parser.add_argument(
        "--end_date",
        type=str,
        required=True,
        help="End date in YYYY-MM format"
    )
    parser.add_argument(
        "--extract_query_template_path",
        type=str,
        required=True,
        help="Path to the SQL extraction query template",
    )
    parser.add_argument(
        "--database_path",
        type=str,
        required=True,
        help="Path to the database"
    )
    parser.add_argument(
        "--source_base_path",
        type=str,
        required=True,
        help="Base path for the remote data files",
    )

    args = parser.parse_args()
    
    extractor = DataExtractor(
        locations_file_path=args.locations_file_path,
        start_date=args.start_date,
        end_date=args.end_date,
        database_path=args.database_path,
        extract_query_template_path=args.extract_query_template_path,
        source_base_path=args.source_base_path
    )
    extractor.extract_data()

if __name__ == "__main__":
    main()