import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import duckdb
import pandas as pd

class AirQualityDashboard:
    def __init__(self):
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        self.db_path = "c:/Users/jeroe/AIR-QUALITY-MONITOR/air_quality.db"
        self.setup_initial_data()
        self.setup_layout()
        self.setup_callbacks()

    def setup_initial_data(self):
        """Initialize data from database"""
        with duckdb.connect(self.db_path, read_only=True) as db_connection:
            self.df = db_connection.execute(
                "SELECT * FROM presentation.air_quality"
            ).fetchdf()
            self.daily_stats_df = db_connection.execute(
                "SELECT * FROM presentation.daily_air_quality_stats"
            ).fetchdf()
            self.latest_values_df = db_connection.execute(
                "SELECT * FROM presentation.latest_param_values_per_location"
            ).fetchdf()
            
        # Rename columns to match expected names
        self.latest_values_df.rename(columns={"lat": "latitude", "lon": "longitude"}, inplace=True)

    def create_map_figure(self):
        """Create the map figure"""
        self.latest_values_df.fillna(0, inplace=True)
        map_fig = px.scatter_map(
            self.latest_values_df,
            lat="latitude",
            lon="longitude",
            hover_name="location",
            hover_data={
                "latitude": True,
                "longitude": True,
                "datetime": True,
                "pm25": True,
            },
            zoom=6.0
        )
        map_fig.update_layout(
            mapbox_style="open-street-map",
            height=800,
            title="Air Quality Monitoring Locations"
        )
        return map_fig

    def setup_layout(self):
        """Setup the dashboard layout"""
        self.app.layout = html.Div([
            dcc.Tabs([
                dcc.Tab(
                    label="Sensor Locations",
                    children=[dcc.Graph(id="map-view")],
                    style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '10px'
                    },
                    selected_style={
                        'backgroundColor': '#e9ecef',
                        'padding': '10px',
                        'borderTop': '3px solid #007bff'
                    }
                ),
                dcc.Tab(
                    label="Parameter Plots",
                    children=[
                        html.Div([
                            html.Div([
                                dcc.Dropdown(
                                    id="location-dropdown",
                                    clearable=False,
                                    multi=False,
                                    searchable=True,
                                    options=self.df["location"].unique(),
                                    value=self.df["location"].unique()[0],
                                    style={'marginBottom': '10px'}
                                ),
                                dcc.Dropdown(
                                    id="parameter-dropdown",
                                    clearable=False,
                                    multi=False,
                                    searchable=True,
                                    options=self.df["parameter"].unique(),
                                    value=self.df["parameter"].unique()[0],
                                    style={'marginBottom': '10px'}
                                ),
                                dcc.DatePickerRange(
                                    id="date-picker-range",
                                    display_format="YYYY-MM-DD",
                                    start_date=self.daily_stats_df["measurement_date"].min(),
                                    end_date=self.daily_stats_df["measurement_date"].max(),
                                    style={'marginBottom': '20px'}
                                ),
                            ], style={
                                'padding': '20px',
                                'backgroundColor': '#ffffff',
                                'borderRadius': '5px',
                                'boxShadow': '0px 0px 5px rgba(0,0,0,0.1)'
                            }),
                            dcc.Graph(id="line-plot"),
                            dcc.Graph(id="box-plot")
                        ], style={'padding': '20px'})
                    ],
                    style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '10px'
                    },
                    selected_style={
                        'backgroundColor': '#e9ecef',
                        'padding': '10px',
                        'borderTop': '3px solid #007bff'
                    }
                )
            ], style={
                'fontFamily': 'Arial, sans-serif',
                'margin': '20px'
            })
        ], style={
            'backgroundColor': '#f8f9fa',
            'minHeight': '100vh',
            'padding': '20px'
        })

    def setup_callbacks(self):
        """Setup all callbacks"""
        @self.app.callback(
            Output("map-view", "figure"),
            Input("map-view", "id")
        )
        def update_map(_):
            return self.create_map_figure()

        @self.app.callback(
            [
                Output("location-dropdown", "options"),
                Output("location-dropdown", "value"),
                Output("parameter-dropdown", "options"),
                Output("parameter-dropdown", "value"),
                Output("date-picker-range", "start_date"),
                Output("date-picker-range", "end_date"),
            ],
            Input("location-dropdown", "id"),
        )
        def update_dropdowns(_):
            with duckdb.connect(self.db_path, read_only=True) as db_connection:
                df = db_connection.execute(
                    "SELECT * FROM presentation.daily_air_quality_stats"
                ).fetchdf()

            location_options = [
                {"label": location, "value": location} for location in df["location"].unique()
            ]
            parameter_options = [
                {"label": parameter, "value": parameter}
                for parameter in df["parameter"].unique()
            ]
            start_date = df["measurement_date"].min()
            end_date = df["measurement_date"].max()

            return (
                location_options,
                df["location"].unique()[0],
                parameter_options,
                df["parameter"].unique()[0],
                start_date,
                end_date,
            )

        @self.app.callback(
            [Output("line-plot", "figure"), Output("box-plot", "figure")],
            [
                Input("location-dropdown", "value"),
                Input("parameter-dropdown", "value"),
                Input("date-picker-range", "start_date"),
                Input("date-picker-range", "end_date")
            ]
        )
        def update_plots(selected_location, selected_parameter, start_date, end_date):
            with duckdb.connect(self.db_path, read_only=True) as db_connection:
                daily_stats_df = db_connection.execute(
                    "SELECT * FROM presentation.daily_air_quality_stats"
                ).fetchdf()

            filtered_df = daily_stats_df[daily_stats_df["location"] == selected_location]
            filtered_df = filtered_df[filtered_df["parameter"] == selected_parameter]
            filtered_df = filtered_df[
                (filtered_df["measurement_date"] >= pd.to_datetime(start_date))
                & (filtered_df["measurement_date"] <= pd.to_datetime(end_date))
            ]

            labels = {
                "average_value": filtered_df["units"].unique()[0],
                "measurement_date": "Date"
            }

            line_fig = px.line(
                filtered_df.sort_values(by="measurement_date"),
                x="measurement_date",
                y="average_value",
                labels=labels,
                title=f"Plot Over Time of {selected_parameter} Levels"
            )

            box_fig = px.box(
                filtered_df.sort_values(by="weekday_number"),
                x="weekday",
                y="average_value",
                labels=labels,
                title=f"Distribution of {selected_parameter} Levels by Weekday"
            )

            return line_fig, box_fig

    def run_server(self, debug=True):
        """Run the dashboard server"""
        self.app.run_server(debug=debug)

if __name__ == "__main__":
    dashboard = AirQualityDashboard()
    dashboard.run_server(debug=True)