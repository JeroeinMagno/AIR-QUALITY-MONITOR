
# AIR QUALITY MONITOR

## Project Overview

This project monitors and visualizes air quality data using OpenAQ. It includes data extraction, transformation, and a Plotly Dash-based dashboard for interactive analysis.

## Prerequisites

Ensure you have the following installed:

- Python (>=3.8)
- pip
- Virtual environment (optional but recommended)
- OpenAQ API key (if required)

## Installation Guide

### 1. Clone the Repository

Download the project to your local machine:

```sh
git clone https://github.com/JeroeinMagno/AIR-QUALITY-MONITOR.git
cd AIR-QUALITY-MONITOR
```

# Project Structure

```
notebooks/         # Scratchpads for experimenting with ideas and testing technologies.
sql/               # SQL scripts for data extraction and transformation, written in DuckDB's query language.
pipeline/          # CLI applications for executing extraction, transformation, and database management tasks.
dashboard/         # Plotly Dash code for creating the live air quality dashboard.
locations.json     # Configuration file containing air quality sensor locations.
secrets-example.json # Example configuration for OpenAQ API keys (Note: Do not commit actual secrets to version control).
requirements.txt   # List of Python libraries and dependencies.
```

# Database Structure

The DuckDB database includes the following schemas and tables:

## Raw Schema
- Contains a single table with all extracted data.

## Presentation Schema
- **air_quality**: The most recent version of each record per location.
- **daily_air_quality_stats**: Daily averages for parameters at each location.
- **latest_param_values_per_location**: Latest values for each parameter at each location.

# Running the Project

Follow these steps to set up and run the project:

## Set Up Python Environment

1. Create a virtual environment:
   ```sh
   python -m venv .venv
   ```
2. Activate the environment:
   - Windows:
     ```sh
     . .venv/Scripts/activate
     ```
   - Linux/Mac:
     ```sh
     . .venv/bin/activate
     ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Initialize the Database

1. Navigate to the pipeline directory:
   ```sh
   cd pipeline
   ```
2. Run the database manager CLI to create the database:
   ```sh
   python database_manager.py --create
   ```

## Extract Data

Run the extraction CLI:
```sh
python extraction.py [required arguments]
```

## Transform Data

Run the transformation CLI to create views in the presentation schema:
```sh
python transformation.py
```

## Set Up the Dashboard

1. Navigate to the dashboard directory:
   ```sh
   cd dashboard
   ```
2. Start the dashboard application:
   ```sh
   python app.py
   ```

## Access the Results

- The database will be stored as a `.db` file.
- The dashboard will be accessible in your web browser.

# Additional Notes

- Ensure Python **3.8+** is installed.
- Replace placeholders (e.g., API keys) in `secrets-example.json` with your actual credentials.
- Regularly update dependencies by running:
  ```sh
  pip install --upgrade -r requirements.txt
  ```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -m 'Description of changes'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any issues, reach out through [GitHub Issues](https://github.com/JeroeinMagno/AIR-QUALITY-MONITOR/issues).
