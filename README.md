
# AeroSync: Interactive Air Quality Monitoring System

## 📚 Table of Contents

1. [Overview](#overview)  
2. [Key Features](#key-features)  
3. [Technologies Used](#technologies-used)  
4. [Setting Up OpenAQ API in Visual Studio Code](#setting-up-openaq-api-in-visual-studio-code)  
5. [Step-by-Step Setup Guide](#step-by-step-setup-guide)  
   - [Obtain an OpenAQ API Key](#1-obtain-an-openaq-api-key)  
   - [Clone the Repository](#2-clone-the-repository)  
   - [Set Up Python Environment in Visual Studio Code](#3-set-up-python-environment-in-visual-studio-code)  
   - [Retrieve Location Coordinates](#4-retrieve-location-coordinates)  
   - [Initialize the Database](#5-initialize-the-database)  
   - [Extract and Transform Data](#6-extract-and-transform-data)  
   - [Open and Run Jupyter Notebook](#7-open-and-run-jupyter-notebook)  
   - [Set Up the Dashboard](#8-set-up-the-dashboard)  
6. [Project Structure](#project-structure)  
7. [Database Structure](#database-structure)  
   - [Raw Schema](#raw-schema)  
   - [Presentation Schema](#presentation-schema)  
8. [Additional Notes](#additional-notes)  
9. [Contributing](#contributing)  
10. [Developers](#developers)  
11. [Acknowledgements](#acknowledgements)  
12. [License](#license)  
13. [Contact](#contact)
    
## Overview
**AeroSync**, is a user-friendly air quality monitoring dashboard that helps users track and assess air conditions. The system collects, processes, and visualizes air quality data through an interactive interface, making it easier to track and evaluate air quality over time.

---

## Key Features

- **Interactive Air Quality Map & User Interaction**  
  Displays air pollution levels using color-coded markers based on PM2.5 concentration levels. The map consists of sensor locations that track air pollution levels. Users can zoom, pan, and hover to explore specific locations and view values such as location name, air quality status, date/time, latitude, longitude, and PM2.5 concentration.

- **Parameter Analysis Dashboard**  
  Allows users to filter air quality data by location, pollutant type (e.g., PM2.5), and date range.

- **Daily Air Quality Statistics**  
  Provides a detailed summary of air quality trends by displaying daily averages, highs, and lows for specific dates. PM2.5 values are categorized as follows:  
  - **Good (≤12.0)** → 🟢 Green  
  - **Moderate (≤35.4)** → 🟠 Orange  
  - **Unhealthy for Sensitive Groups (≤55.4)** → 🔶 Dark Orange  
  - **Unhealthy (>55.4)** → 🔴 Red  

---
## Technologies Used

AeroSync is built using a combination of modern technologies to ensure efficient data processing, visualization, and user interaction.

### **Programming Languages**
- **Python** – Used for backend processing, data extraction, transformation, and dashboard development.

### **Data Handling & Storage**
- **DuckDB** – Lightweight and high-performance database engine used for storing and querying air quality data.
- **Pandas** – Utilized for data manipulation and analysis.
- **OpenAQ API** – Provides air quality data for various locations worldwide.

### **Web Development & Visualization**
- **Plotly** – A graphing library for creating interactive charts and visualizations used in the dashboard.
- **Dash** – A Python framework built on top of Flask, React, and Plotly, used to develop interactive web applications and dashboards.

### **Version Control & Deployment**
- **Git & GitHub** – Used for version control and collaboration.
- **Virtual Environment (venv)** – Ensures dependency isolation for a stable development environment.

These technologies collectively enable AeroSync to efficiently collect, store, analyze, and visualize air quality data while providing users with an intuitive and interactive experience. 🚀

---
## Setting Up OpenAQ API in Visual Studio Code

### Prerequisites

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

## Developers
</h2>

| **Name**                 | **GitHub**                                                       | **Other Contacts**                                                                 |
|--------------------------|------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Evangelista, Aeron M.          | [Evangelista, Aeron M. ](https://github.com/AeronEvangelista)          | [Evangelista, Aeron M. ](https://www.facebook.com/mr.poginglamig)|
| Lajara, Chester P.      | [Lajara, Chester P.](https://github.com/Chesterlajara)          | [Lajara, Chester P.](https://www.facebook.com/chistirrrrr)|
| Magno, Jeroein Lloyd P.          | [Magno, Jeroein Lloyd P.](https://github.com/AeronEvangelista)          | [Magno, Jeroein Lloyd P.](https://www.facebook.com/jeroeinmagno1429)|
---

## Acknowledgements
**Course Instructor.** The researchers would like to express their sincere gratitude to their instructor, Ms. Fatima Marie P. Agdon, MSCS, for her invaluable guidance, support, and encouragement throughout this research. Her expertise and insights have been crucial in shaping the development of AeroSync and ensuring the success of this research study.

**Peers and Colleagues.** The researchers also extend their appreciation to their peers and colleagues for their constructive feedback, insightful discussions, and shared knowledge, which have contributed to the refinement and improvement of this research study.

**Family and Friends.** Furthermore, the researchers are deeply grateful to their families and friends for their unwavering support throughout the research process.

**Research Contributors.** Lastly, appreciation is given to the various researchers, organizations, and data sources that provided essential information on air quality and environmental monitoring, which served as a vital foundation for this study.

With sincere gratitude, the researchers acknowledge all those who have played a part in the success of this research.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For any issues, reach out through [GitHub Issues](https://github.com/JeroeinMagno/AIR-QUALITY-MONITOR/issues).

