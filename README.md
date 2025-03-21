
# AeroSync: Interactive Air Quality Monitoring System

## Table of Contents

- Overview
- Key Features
- Acknowledgement

## Overview
**AeroSync**, is a user-friendly air quality monitoring dashboard that helps users track and assess air conditions. The system collects, processes, and visualizes air quality data through an interactive interface, making it easier to track and evaluate air quality over time.

## Key Features
- Interactive Air Quality Map & User Interaction  
- Parameter Analysis Dashboard
-  Daily Air Quality Statistics

## Acknowledgement
**Course Instructor.** The researchers would like to express their sincere gratitude to their instructor, Ms. Fatima Marie P. Agdon, MSCS, for her invaluable guidance, support, and encouragement throughout this research. Her expertise and insights have been crucial in shaping the development of AeroSync and ensuring the success of this research study.

**Peers and Colleagues.** The researchers also extend their appreciation to their peers and colleagues for their constructive feedback, insightful discussions, and shared knowledge, which have contributed to the refinement and improvement of this research study.

**Family and Friends.** Furthermore, the researchers are deeply grateful to their families and friends for their unwavering support throughout the research process.

**Research Contributors.** Lastly, appreciation is given to the various researchers, organizations, and data sources that provided essential information on air quality and environmental monitoring, which served as a vital foundation for this study.

With sincere gratitude, the researchers acknowledge all those who have played a part in the success of this research.



# Setting Up OpenAQ API in Visual Studio Code

## Prerequisites
Ensure you have the following installed:
- **Python (>=3.8)**
- **pip**
- **Virtual environment (optional but recommended)**
- **OpenAQ API key** (if required)
- **Git** (for version control)

## Step-by-Step Setup Guide

### 1. Obtain an OpenAQ API Key
1. Go to the [OpenAQ Documentation](https://docs.openaq.org/).
2. Sign in and generate an API key.
3. Store the API key securely. Do not expose it in public repositories.
4. Create a file named `secrets.json` and add your API key:
   ```json
   {
       "openaq-api-key": "your-api-key-here"
   }
   ```
5. Add `secrets.json` to `.gitignore` to prevent accidental exposure.

### 2. Clone the Repository
1. Open **VS Code** and navigate to the terminal.
2. Clone the repository:
   ```sh
   git clone https://github.com/JeroeinMagno/AIR-QUALITY-MONITOR.git
   ```
3. Navigate to the project folder:
   ```sh
   cd AIR-QUALITY-MONITOR
   ```

### 3. Set Up Python Environment in Visual Studio Code
1. Check your Python version:
   ```sh
   python --version
   ```
   Ensure you have Python 3.8 or higher installed.
2. Create a virtual environment:
   ```sh
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - **Windows:**
     ```sh
     . .venv/Scripts/activate
     ```
   - **Linux/Mac:**
     ```sh
     . .venv/bin/activate
     ```
4. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```

### 4. Retrieve Location Coordinates
1. Use [BBoxFinder](http://bboxfinder.com/) to select a specific area.
2. Draw a rectangle over your target location.
3. Copy the latitude and longitude values.
4. Store them in `notebooks/api-exploration.ipynb` for later use.

### 5. Initialize the Database
1. Navigate to the `pipeline` directory:
   ```sh
   cd pipeline
   ```
2. Run the database manager CLI to create the database:
   ```sh
   python database_manager.py --create
   ```

### 6. Extract and Transform Data
1. Extract data from OpenAQ API:
   ```sh
   python extraction.py [required arguments] 
   ```
   Example usage: python extraction.py --locations_file_path ../location.json --start_date 2024-01 --end_date 2025-01 --database_path ../air_quality.db --extract_query_template_path ../sql/dml/raw/0_raw_air_quality_insert.sql --source_base_path s3://openaq-data-archive/records/csv.gz
   
3. Transform the extracted data:
   ```sh
   python transformation.py
   ```

### 7. Open and Run Jupyter Notebook
1. Launch Jupyter Notebook:
   ```sh
   jupyter notebook
   ```
2. Open `notebooks/api-exploration.ipynb`.
3. Select the virtual environment kernel (`.venv`).
4. Run all cells to ensure the setup is correct.

### 8. Set Up the Dashboard
1. Navigate to the `dashboard` directory:
   ```sh
   cd dashboard
   ```
2. Start the dashboard application:
   ```sh
   python app.py
   ```
3. Open your web browser and access the dashboard.

## Project Structure
```
notebooks/         # Scratchpads for experimenting with ideas and testing technologies.
sql/               # SQL scripts for data extraction and transformation, written in DuckDB's query language.
pipeline/          # CLI applications for executing extraction, transformation, and database management tasks.
dashboard/         # Plotly Dash code for creating the live air quality dashboard.
locations.json     # Configuration file containing air quality sensor locations.
secrets-example.json # Example configuration for OpenAQ API keys (Note: Do not commit actual secrets to version control).
requirements.txt   # List of Python libraries and dependencies.
```

## Database Structure
The DuckDB database includes the following schemas and tables:

### Raw Schema
- Contains a single table with all extracted data.

### Presentation Schema
- **air_quality**: The most recent version of each record per location.
- **daily_air_quality_stats**: Daily averages for parameters at each location.
- **latest_param_values_per_location**: Latest values for each parameter at each location.

## Additional Notes
- Always replace placeholders (e.g., API keys) in `secrets.json` with actual credentials.
- Update dependencies regularly:
  ```sh
  pip install --upgrade -r requirements.txt
  ```
- The `.gitignore` file is crucial for hiding credentials and preventing security risks.

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

