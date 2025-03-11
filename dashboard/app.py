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
        """Create the map figure with categorized PM2.5 values"""
        self.latest_values_df.fillna(0, inplace=True)
        
        def categorize_pm25(value):
            if value <= 12.0:
                return "Good"
            elif value <= 35.4:
                return "Moderate"
            elif value <= 55.4:
                return "Unhealthy for Sensitive Groups"
            else:
                return "Unhealthy"
        
        # Create color mapping dictionary
        color_map = {
            "Good": "#00E400",  # Green
            "Moderate": "#FFAA1C",  # Orange
            "Unhealthy for Sensitive Groups": "#FF7E00",  # Dark Orange
            "Unhealthy": "#FF0000"  # Red
        }
        
        # Add air quality status column
        self.latest_values_df["air_quality_status"] = self.latest_values_df["pm25"].apply(categorize_pm25)
        
        # Create the scatter mapbox figure
        map_fig = px.scatter_mapbox(
        self.latest_values_df,
        lat="latitude",
        lon="longitude",
        hover_name="location",
        color="air_quality_status",
        color_discrete_map=color_map,
        hover_data={
            "latitude": ":.4f",
            "longitude": ":.4f",
            "datetime": True,
            "air_quality_status": True,
            "pm25": ":.1f"
        },
        zoom=6.0,
        size=[15] * len(self.latest_values_df),  # Set uniform size for all markers
        size_max=15  # Increase maximum marker size
    )
        
        # Update the layout with enhanced styling
        map_fig.update_layout(
        mapbox_style="open-street-map",
        height=800,           
        legend_title={
            'text': "Air Quality Status",
            'font': {'size': 16, 'color': '#2c3e50'}
        },
        margin={'r': 0, 'l': 0, 'b': 0, 't': 40},
        legend={
            'x': 0.01,  # Move legend to the left
            'y': 0.99,  # Keep at top
            'xanchor': 'left',  # Anchor point on the left
            'yanchor': 'top',   # Anchor point at top
            'bgcolor': 'rgba(255, 255, 255, 0.8)',  # Semi-transparent white background
            'bordercolor': '#2c3e50',  # Border color
            'borderwidth': 1  # Border width (changed from 'border')
        }
    )
        
        return map_fig

    def setup_layout(self):
        self.app.layout = html.Div([
        # Add this interval component at the top of your layout
        dcc.Interval(
            id='interval-component',
            interval=300000,  # 5 minutes in milliseconds
            n_intervals=0
        ),

        dbc.Alert(
            "Last updated: Auto-refresh every 5 minutes",
            id="refresh-alert",
            color="info",
            dismissable=True,
            className="text-center mb-3"
        ),
            html.Div([
                html.H1(
                    "Air Quality Monitoring Dashboard",
                    className="text-center mb-4",
                    style={
                        'color': '#2c3e50',
                        'fontWeight': 'bold',
                        'fontSize': '2.5rem'
                    }
                ),
                html.Hr(style={'borderColor': '#007bff'})
            ], style={
                'padding': '20px 0',
                'background': 'linear-gradient(to right, #f8f9fa, #e9ecef)'
            }),

            # Main content
            dcc.Tabs([
                # Map Tab
                dcc.Tab(
                    label="📍 Sensor Locations",
                    children=[
                        html.Div([
                            html.H3(
                                className="text-center mb-3",
                                style={'color': '#2c3e50'}
                            ),
                            dcc.Graph(
                                id="map-view",
                                config={
                                    'displayModeBar': True,
                                    'scrollZoom': True,
                                    'modeBarButtonsToRemove': ['select2d', 'lasso2d']
                                }
                            )
                        ], className="p-4 shadow-sm")
                    ],
                    style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '10px',
                        'borderRadius': '5px'
                    },
                    selected_style={
                        'backgroundColor': '#e9ecef',
                        'padding': '10px',
                        'borderTop': '3px solid #007bff',
                        'borderRadius': '5px'
                    }
                ),

                # Parameters Tab with enhanced styling
                dcc.Tab(
                    label="📊 Parameter Analysis",
                    children=[
                        html.Div([
                            # Control Panel with shadow
                            dbc.Card([
                                dbc.CardBody([
                                    html.H4(
                                        "Filter Controls",
                                        className="card-title mb-3",
                                        style={'color': '#2c3e50'}
                                    ),
                                    html.Div([
                                        html.Label(
                                            "Location:",
                                            className="font-weight-bold d-block mb-2",
                                            style={'color': '#495057'}
                                        ),
                                        dcc.Dropdown(
                                            id="location-dropdown",
                                            clearable=False,
                                            multi=False,
                                            searchable=True,
                                            options=self.df["location"].unique(),
                                            value=self.df["location"].unique()[0],
                                            className="mb-3"
                                        ),
                                        html.Label(
                                            "Parameter:",
                                            className="font-weight-bold d-block mb-2",
                                            style={'color': '#495057'}
                                        ),
                                        dcc.Dropdown(
                                            id="parameter-dropdown",
                                            clearable=False,
                                            multi=False,
                                            searchable=True,
                                            options=self.df["parameter"].unique(),
                                            value=self.df["parameter"].unique()[0],
                                            className="mb-3"
                                        ),
                                        html.Label(
                                            "Date Range:",
                                            className="font-weight-bold d-block mb-2",
                                            style={'color': '#495057'}
                                        ),
                                        dcc.DatePickerRange(
                                            id="date-picker-range",
                                            display_format="YYYY-MM-DD",
                                            start_date=self.daily_stats_df["measurement_date"].min(),
                                            end_date=self.daily_stats_df["measurement_date"].max(),
                                            className="mb-3"
                                        )
                                    ])
                                ])
                            ], className="mb-4 shadow-sm", style={'backgroundColor': '#ffffff'}),

                            # Graphs Container with enhanced cards
                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardBody([
                                            dcc.Graph(id="line-plot")
                                        ])
                                    ], className="mb-4 shadow-sm")
                                ], md=12),
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardBody([
                                            dcc.Graph(id="box-plot")
                                        ])
                                    ], className="mb-4 shadow-sm")
                                ], md=12)
                            ])
                        ], style={'padding': '20px'})
                    ],
                    style={
                        'backgroundColor': '#f8f9fa',
                        'padding': '10px',
                        'borderRadius': '5px'
                    },
                    selected_style={
                        'backgroundColor': '#e9ecef',
                        'padding': '10px',
                        'borderTop': '3px solid #007bff',
                        'borderRadius': '5px'
                    }
                )
            ], className="mb-4")
        ], style={
            'backgroundColor': '#f0f2f5',
            'minHeight': '100vh',
            'fontFamily': '"Segoe UI", Arial, sans-serif',
            'padding': '20px'
        })

    def setup_callbacks(self):
        # Add refresh time callback
        @self.app.callback(
            Output("refresh-alert", "children"),
            Input("interval-component", "n_intervals")
        )
        def update_refresh_time(n):
            return f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} (Auto-refresh every 5 minutes)"

        # Map view callback
        @self.app.callback(
            Output("map-view", "figure"),
            [Input("map-view", "id"),
             Input("interval-component", "n_intervals")]
        )
        def update_map(_, n):
            # Refresh data from database
            with duckdb.connect(self.db_path, read_only=True) as db_connection:
                self.latest_values_df = db_connection.execute(
                    "SELECT * FROM presentation.latest_param_values_per_location"
                ).fetchdf()
                self.latest_values_df.rename(columns={"lat": "latitude", "lon": "longitude"}, inplace=True)
            return self.create_map_figure()

        # Dropdown options callback
        @self.app.callback(
            [
                Output("location-dropdown", "options"),
                Output("location-dropdown", "value"),
                Output("parameter-dropdown", "options"),
                Output("parameter-dropdown", "value"),
                Output("date-picker-range", "start_date"),
                Output("date-picker-range", "end_date"),
            ],
            [Input("location-dropdown", "id"),
             Input("interval-component", "n_intervals")]
        )
        def update_dropdowns(_, n):
            with duckdb.connect(self.db_path, read_only=True) as db_connection:
                df = db_connection.execute(
                    "SELECT * FROM presentation.daily_air_quality_stats"
                ).fetchdf()

                location_options = [
                    {"label": location, "value": location} 
                    for location in df["location"].unique()
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

        # Unified plots callback
        @self.app.callback(
            [Output("line-plot", "figure"), 
             Output("box-plot", "figure")],
            [
                Input("location-dropdown", "value"),
                Input("parameter-dropdown", "value"),
                Input("date-picker-range", "start_date"),
                Input("date-picker-range", "end_date"),
                Input("interval-component", "n_intervals")
            ]
        )
        def update_plots(selected_location, selected_parameter, start_date, end_date, n):
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

            def categorize_pm25(value):
                if value <= 12.0:
                    return f"{value:.1f} (Good)"
                elif value <= 35.4:
                    return f"{value:.1f} (Moderate)"
                elif value <= 55.4:
                    return f"{value:.1f} (Unhealthy for Sensitive Groups)"
                else:
                    return f"{value:.1f} (Unhealthy)"

            if selected_parameter == "pm25":
                filtered_df["display_value"] = filtered_df["average_value"].apply(categorize_pm25)
            else:
                filtered_df["display_value"] = filtered_df["average_value"]

            labels = {
                "average_value": filtered_df["units"].unique()[0],
                "measurement_date": "Date",
                "display_value": f"{selected_parameter} Level"
            }

            line_fig = px.line(
                filtered_df.sort_values(by="measurement_date"),
                x="measurement_date",
                y="average_value",
                labels=labels,
                title=f"Plot Over Time of {selected_parameter} Levels",
                custom_data=["display_value"]
            )
            
            line_fig.update_traces(
                hovertemplate="<br>".join([
                    "Date: %{x}",
                    "Value: %{customdata[0]}",
                    "<extra></extra>"
                ])
            )

            box_fig = px.box(
                filtered_df.sort_values(by="weekday_number"),
                x="weekday",
                y="average_value",
                labels=labels,
                title=f"Distribution of {selected_parameter} Levels by Weekday",
                custom_data=["display_value"]
            )
            
            box_fig.update_traces(
                hovertemplate="<br>".join([
                    "Weekday: %{x}",
                    "Value: %{customdata[0]}",
                    "<extra></extra>"
                ])
            )

            return line_fig, box_fig

    def run_server(self, debug=True):
        """Run the dashboard server"""
        self.app.run_server(debug=debug)

if __name__ == "__main__":
    dashboard = AirQualityDashboard()
    dashboard.run_server(debug=True)