CREATE OR REPLACE VIEW presentation.air_quality AS (
    WITH ranked_data AS (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY location_id, sensor_id, "datetime", "parameter"
                ORDER BY ingestion_datetime DESC
            ) AS rn
        FROM raw.air_quality
        WHERE parameter IN ('pm25')
        AND "value" >= 0
    )
    SELECT
        location_id,
        sensor_id,
        "location",
        "datetime",
        latitude AS lat,
        longitude AS lon,
        lon,
        "parameter",
        units,
        "value",
        "month",
        "year",
        ingestion_datetime
    FROM ranked_data
    WHERE rn = 1
);