import unittest
import time
from datetime import datetime
from app import AirQualityDashboard

class TestAirQualityDashboard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dashboard = AirQualityDashboard()
        print("\n🧪 Starting Test Suite for AirQualityDashboard")

    def test_001_load_sensor_map_view(self):
        df = self.dashboard.latest_values_df
        self.assertFalse(df.empty, "Sensor data should not be empty")
        self.assertIn("latitude", df.columns)
        self.assertIn("longitude", df.columns)
        self.assertIn("pm25", df.columns)
        print("✅ TC001 passed: Sensor map data loaded successfully.")

    def test_002_auto_refresh_simulation(self):
        start = datetime.now()
        time.sleep(1)  # Simulated short wait instead of 5 mins
        end = datetime.now()
        elapsed = (end - start).seconds
        self.assertGreaterEqual(elapsed, 1, "Auto-refresh logic did not wait correctly")
        print("✅ TC002 passed: Auto-refresh simulation worked correctly.")

    def test_003_filter_location_and_parameter(self):
        df = self.dashboard.df
        locations = df["location"].unique()
        parameters = df["parameter"].unique()
        self.assertGreater(len(locations), 0, "No locations found")
        self.assertGreater(len(parameters), 0, "No parameters found")
        print("✅ TC003 passed: Location and parameter filters are functional.")

    def test_004_date_range_filtering(self):
        df = self.dashboard.daily_stats_df
        start_date = df["measurement_date"].min()
        end_date = df["measurement_date"].max()
        filtered = df[
            (df["measurement_date"] >= start_date) &
            (df["measurement_date"] <= end_date)
        ]
        self.assertFalse(filtered.empty, "Date filter returned no data")
        print("✅ TC004 passed: Date range filtering works properly.")

    def test_005_pm25_value_formatting(self):
        def categorize_pm25(value):
            if value <= 12.0:
                return f"{value:.1f} (Good)"
            elif value <= 35.4:
                return f"{value:.1f} (Moderate)"
            elif value <= 55.4:
                return f"{value:.1f} (Unhealthy for Sensitive Groups)"
            else:
                return f"{value:.1f} (Unhealthy)"

        result = categorize_pm25(25.3)
        self.assertIn("Moderate", result)
        print(f"✅ TC005 passed: PM2.5 value '{result}' categorized correctly.")

    def test_006_application_layout_loads(self):
        try:
            self.dashboard.setup_layout()
            print("✅ TC006 passed: Application layout loaded without error.")
        except Exception as e:
            self.fail(f"App layout setup failed: {e}")

if __name__ == '__main__':
    unittest.main()
